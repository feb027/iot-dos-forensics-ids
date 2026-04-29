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
BASELINE_METRICS = ROOT / "results" / "tables" / "baseline_model_metrics.csv"
BASELINE_CONFUSION = ROOT / "results" / "tables" / "baseline_confusion_matrices.csv"
BASELINE_SUMMARY = ROOT / "results" / "metrics" / "baseline_summary.json"
FORENSIC_FEATURE_IMPORTANCE = ROOT / "results" / "tables" / "forensic_feature_importance.csv"
FORENSIC_ERROR_ANALYSIS = ROOT / "results" / "tables" / "forensic_error_analysis.csv"
FORENSIC_SUMMARY = ROOT / "results" / "metrics" / "forensic_summary.json"
ADVANCED_METRICS = ROOT / "results" / "tables" / "advanced_model_metrics.csv"
ADVANCED_CONFUSION = ROOT / "results" / "tables" / "advanced_confusion_matrices.csv"
ADVANCED_SHAP_SUMMARY = ROOT / "results" / "tables" / "advanced_shap_summary.csv"
ADVANCED_SUMMARY = ROOT / "results" / "metrics" / "advanced_summary.json"


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


def load_baseline_results() -> tuple[list[dict], list[dict], dict]:
    model_comparison: list[dict] = []
    confusion_matrix: list[dict] = []
    baseline_summary: dict = {}

    if BASELINE_METRICS.exists() and BASELINE_METRICS.read_text(encoding="utf-8").strip():
        with BASELINE_METRICS.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                model_comparison.append(
                    {
                        "track": row["track"],
                        "model": row["model"],
                        "model_display_name": row.get("model_display_name", row["model"]),
                        "model_family": row.get("model_family", ""),
                        "macro_f1": float(row["macro_f1"]),
                        "mcc": float(row["mcc"]),
                        "balanced_accuracy": float(row["balanced_accuracy"]),
                        "precision_attack": float(row["precision_attack"]),
                        "recall_attack": float(row["recall_attack"]),
                        "precision_normal": float(row["precision_normal"]),
                        "recall_normal": float(row["recall_normal"]),
                        "accuracy": float(row["accuracy"]),
                    }
                )
        model_comparison.sort(key=lambda r: (r["macro_f1"], r["mcc"], r["recall_normal"]), reverse=True)

    if BASELINE_CONFUSION.exists() and BASELINE_CONFUSION.read_text(encoding="utf-8").strip():
        with BASELINE_CONFUSION.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                confusion_matrix.append(
                    {
                        "track": row["track"],
                        "model": row["model"],
                        "tn_normal_correct": int(row["tn_normal_correct"]),
                        "fp_normal_as_attack": int(row["fp_normal_as_attack"]),
                        "fn_attack_as_normal": int(row["fn_attack_as_normal"]),
                        "tp_attack_correct": int(row["tp_attack_correct"]),
                    }
                )

    if BASELINE_SUMMARY.exists():
        baseline_summary = json.loads(BASELINE_SUMMARY.read_text(encoding="utf-8"))

    return model_comparison, confusion_matrix, baseline_summary


def load_forensic_results() -> tuple[list[dict], list[dict], dict]:
    feature_importance: list[dict] = []
    error_analysis: list[dict] = []
    forensic_summary: dict = {}

    if FORENSIC_FEATURE_IMPORTANCE.exists() and FORENSIC_FEATURE_IMPORTANCE.read_text(encoding="utf-8").strip():
        with FORENSIC_FEATURE_IMPORTANCE.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("method") == "tree_feature_importance":
                    feature_importance.append(
                        {
                            "track": row["track"],
                            "model": row["model"],
                            "method": row["method"],
                            "rank": int(row["rank"]),
                            "feature": row["feature"],
                            "feature_group": row["feature_group"],
                            "importance": float(row["importance"]),
                            "normalized_importance": float(row.get("normalized_importance") or 0),
                            "interpretation_hint": row.get("interpretation_hint", ""),
                        }
                    )
        feature_importance.sort(key=lambda r: (r["normalized_importance"], r["importance"]), reverse=True)

    if FORENSIC_ERROR_ANALYSIS.exists() and FORENSIC_ERROR_ANALYSIS.read_text(encoding="utf-8").strip():
        with FORENSIC_ERROR_ANALYSIS.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                error_analysis.append(
                    {
                        "track": row["track"],
                        "model": row["model"],
                        "error_type": row["error_type"],
                        "count": int(row["count"]),
                        "rate_of_track_test": float(row["rate_of_track_test"]),
                        "top_proto": row.get("top_proto", ""),
                        "top_category": row.get("top_category", ""),
                    }
                )

    if FORENSIC_SUMMARY.exists():
        forensic_summary = json.loads(FORENSIC_SUMMARY.read_text(encoding="utf-8"))

    return feature_importance, error_analysis, forensic_summary


def load_advanced_results() -> tuple[list[dict], list[dict], list[dict], dict]:
    advanced_models: list[dict] = []
    advanced_confusion: list[dict] = []
    advanced_shap: list[dict] = []
    advanced_summary: dict = {}

    if ADVANCED_METRICS.exists() and ADVANCED_METRICS.read_text(encoding="utf-8").strip():
        with ADVANCED_METRICS.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                advanced_models.append(
                    {
                        "track": row["track"],
                        "model": row["model"],
                        "model_display_name": row.get("model_display_name", row["model"]),
                        "model_family": row.get("model_family", ""),
                        "macro_f1": float(row["macro_f1"]),
                        "mcc": float(row["mcc"]),
                        "balanced_accuracy": float(row["balanced_accuracy"]),
                        "precision_attack": float(row["precision_attack"]),
                        "recall_attack": float(row["recall_attack"]),
                        "precision_normal": float(row["precision_normal"]),
                        "recall_normal": float(row["recall_normal"]),
                        "accuracy": float(row["accuracy"]),
                        "baseline_best_model_for_track": row.get("baseline_best_model_for_track", ""),
                        "baseline_macro_f1_for_track": float(row.get("baseline_macro_f1_for_track") or 0),
                        "delta_macro_f1_vs_baseline": float(row.get("delta_macro_f1_vs_baseline") or 0),
                        "delta_mcc_vs_baseline": float(row.get("delta_mcc_vs_baseline") or 0),
                    }
                )
        advanced_models.sort(key=lambda r: (r["macro_f1"], r["mcc"], r["recall_normal"]), reverse=True)

    if ADVANCED_CONFUSION.exists() and ADVANCED_CONFUSION.read_text(encoding="utf-8").strip():
        with ADVANCED_CONFUSION.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                advanced_confusion.append(
                    {
                        "track": row["track"],
                        "model": row["model"],
                        "tn_normal_correct": int(row["tn_normal_correct"]),
                        "fp_normal_as_attack": int(row["fp_normal_as_attack"]),
                        "fn_attack_as_normal": int(row["fn_attack_as_normal"]),
                        "tp_attack_correct": int(row["tp_attack_correct"]),
                    }
                )

    if ADVANCED_SHAP_SUMMARY.exists() and ADVANCED_SHAP_SUMMARY.read_text(encoding="utf-8").strip():
        with ADVANCED_SHAP_SUMMARY.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                advanced_shap.append(
                    {
                        "track": row["track"],
                        "model": row["model"],
                        "method": row["method"],
                        "rank": int(row["rank"]),
                        "feature": row["feature"],
                        "feature_group": row["feature_group"],
                        "mean_abs_shap": float(row["mean_abs_shap"]),
                        "normalized_mean_abs_shap": float(row["normalized_mean_abs_shap"]),
                        "sample_rows": int(float(row["sample_rows"])),
                        "interpretation_hint": row.get("interpretation_hint", ""),
                    }
                )
        advanced_shap.sort(key=lambda r: (r["normalized_mean_abs_shap"], r["mean_abs_shap"]), reverse=True)

    if ADVANCED_SUMMARY.exists():
        advanced_summary = json.loads(ADVANCED_SUMMARY.read_text(encoding="utf-8"))

    return advanced_models, advanced_confusion, advanced_shap, advanced_summary


def main() -> None:
    dataset_summary, class_distribution = load_dataset_audit()
    eda_summary = load_eda_summary()
    model_comparison, confusion_matrix, baseline_summary = load_baseline_results()
    feature_importance, forensic_error_analysis, forensic_summary = load_forensic_results()
    advanced_models, advanced_confusion, advanced_shap, advanced_summary = load_advanced_results()
    if advanced_summary:
        status = "Fase 6A merged; Fase 6 dashboard polish current"
    elif forensic_summary:
        status = "Fase 6A Advanced/SOTA Modeling current; Fase 5 merged"
    elif model_comparison:
        status = "Fase 5 Forensic Analysis current; baseline modeling completed"
    elif eda_summary:
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
        "model_comparison": model_comparison,
        "confusion_matrix": confusion_matrix,
        "feature_importance": feature_importance[:30],
        "baseline_summary": baseline_summary,
        "forensic_error_analysis": forensic_error_analysis,
        "forensic_summary": forensic_summary,
        "advanced_models": advanced_models,
        "advanced_confusion": advanced_confusion,
        "advanced_shap": advanced_shap[:30],
        "advanced_summary": advanced_summary,
        "forensic_notes": (
            [
                "Fase 5 telah menghasilkan feature importance dan error analysis dari selected baseline runs.",
                "Interpretasi forensik tetap dibatasi oleh normal class kecil dan split-similarity risk.",
            ] if forensic_summary else [
                "Fase 4 telah menghasilkan baseline metrics dan confusion matrix untuk Track A/B/C.",
                "Fase 5 berjalan: feature importance dan error analysis akan dipakai untuk interpretasi forensik DoS/DDoS.",
            ]
        ) if eda_summary else ([
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
