from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dashboard" / "data" / "dashboard-data.json"
AUDIT_METRICS = ROOT / "results" / "metrics" / "dataset_audit.json"
PREPROCESSING_METRICS = ROOT / "results" / "metrics" / "preprocessing_summary.json"
CLASS_DISTRIBUTION = ROOT / "results" / "tables" / "class_distribution.csv"
EDA_SCOPE_DISTRIBUTION = ROOT / "results" / "tables" / "eda_binary_scope_distribution.csv"
PREPROCESSING_DATASET_PLAN = ROOT / "results" / "tables" / "preprocessing_dataset_plan.csv"


def load_dataset_audit() -> tuple[dict, list[dict]]:
    if not AUDIT_METRICS.exists():
        return {}, []

    metrics = json.loads(AUDIT_METRICS.read_text(encoding="utf-8"))
    files = metrics.get("files", [])
    total_rows = sum(int(f.get("rows", 0)) for f in files)
    total_bytes = sum(int(f.get("bytes", 0)) for f in files)
    dataset_summary = {
        "source": metrics.get("source_name"),
        "official_primary_source": metrics.get("official_primary_source"),
        "working_mirror": metrics.get("working_mirror"),
        "rows": total_rows,
        "files": len(files),
        "bytes": total_bytes,
        "columns": files[0].get("columns") if files else None,
        "candidate_features": len(metrics.get("recommended_candidate_features", [])),
        "excluded_columns": metrics.get("recommended_excluded_columns_for_baseline", []),
    }

    class_distribution = []
    if CLASS_DISTRIBUTION.exists():
        with CLASS_DISTRIBUTION.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("group") in {"category_counts", "dos_scope_counts"}:
                    class_distribution.append(
                        {
                            "split": row["split"],
                            "group": row["group"],
                            "label": row["label"],
                            "count": int(row["count"]),
                            "rate": float(row["rate"]),
                        }
                    )
    return dataset_summary, class_distribution


def load_eda_summary() -> dict:
    if not PREPROCESSING_METRICS.exists():
        return {}
    metrics = json.loads(PREPROCESSING_METRICS.read_text(encoding="utf-8"))
    scope_counts: dict[str, dict[str, int]] = {}
    if EDA_SCOPE_DISTRIBUTION.exists():
        with EDA_SCOPE_DISTRIBUTION.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                scope_counts.setdefault(row["split"], {})[row["scope"]] = int(row["count"])

    dataset_plan = []
    if PREPROCESSING_DATASET_PLAN.exists():
        with PREPROCESSING_DATASET_PLAN.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["track"] in {"A_realistic_imbalanced", "B_balanced_controlled_1_to_1", "C_balanced_controlled_1_to_2"}:
                    dataset_plan.append(row)

    return {
        "total_rows": metrics.get("total_rows"),
        "candidate_features": metrics.get("candidate_features", []),
        "excluded_columns": metrics.get("excluded_columns", []),
        "recommended_phase4_tracks": metrics.get("recommended_phase4_tracks", []),
        "warnings": metrics.get("warnings", []),
        "scope_counts": scope_counts,
        "dataset_plan": dataset_plan,
        "figures": metrics.get("outputs", {}).get("figures", []),
    }


def main() -> None:
    dataset_summary, class_distribution = load_dataset_audit()
    eda_summary = load_eda_summary()
    if eda_summary:
        status = "Fase 4 Baseline Modeling current; no model results yet"
    elif dataset_summary:
        status = "Fase 3 EDA & Preprocessing ready; modeling not started"
    else:
        status = "Fase 1 literature review approved; Fase 2 dataset audit pending"
    data = {
        "project": {
            "title": "Sistem Analisis Serangan DoS pada Arsitektur IoT",
            "theme": "IoT + Cyber Security + Digital Forensics",
            "primary_dataset": "BoT-IoT (UNSW)",
            "alternative_dataset": "RT-IoT2022 (UCI)",
            "status": status,
        },
        "dataset_summary": dataset_summary,
        "class_distribution": class_distribution,
        "eda_summary": eda_summary,
        "model_comparison": [],
        "confusion_matrix": {},
        "feature_importance": [],
        "forensic_notes": [
            "Fase 3 menyiapkan dua jalur eksperimen: distribusi asli yang sangat imbalanced dan controlled balanced subset untuk mitigasi normal class kecil.",
            "Hasil forensik detail akan diisi setelah feature importance dan error analysis tersedia.",
        ] if eda_summary else ([
            "Fase 2 menemukan risiko utama: class imbalance ekstrem dan kemiripan fitur agregat antar split; mitigasi harus diterapkan sebelum modeling.",
            "Hasil forensik detail akan diisi setelah feature importance dan error analysis tersedia.",
        ] if dataset_summary else [
            "Hasil forensik akan diisi setelah feature importance dan error analysis tersedia."
        ]),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
