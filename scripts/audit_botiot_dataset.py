#!/usr/bin/env python3
"""Audit BoT-IoT/UNSW-IoT CSV splits without loading the full dataset into pandas.

The script is intentionally stdlib-only so it can run on VPS, WSL2, or Colab
before heavy ML dependencies are installed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

DEFAULT_FILES = ["train.csv", "test.csv"]
LABEL_COLUMNS = {"attack", "category", "subcategory"}
ID_COLUMNS = {"pkSeqID", "seq"}
NETWORK_IDENTIFIER_COLUMNS = {"saddr", "sport", "daddr", "dport"}
HIGH_LEAKAGE_COLUMNS = LABEL_COLUMNS | ID_COLUMNS | NETWORK_IDENTIFIER_COLUMNS
DOS_CATEGORIES = {"DoS", "DDoS"}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_hash(values: Iterable[str]) -> str:
    # Use a separator unlikely to occur in CSV network fields.
    joined = "\x1f".join(values)
    return hashlib.blake2b(joined.encode("utf-8", errors="replace"), digest_size=16).hexdigest()


def is_missing(value: str) -> bool:
    return value == "" or value.lower() in {"na", "nan", "null", "none", "?"}


def infer_type(value: str) -> str:
    if is_missing(value):
        return "missing"
    try:
        int(value)
        return "integer"
    except ValueError:
        pass
    try:
        float(value)
        return "float"
    except ValueError:
        return "categorical"


def dos_scope_label(row: dict[str, str]) -> str:
    attack = row.get("attack", "")
    category = row.get("category", "")
    if attack in {"0", "0.0"} or category.lower() == "normal":
        return "normal"
    if category in DOS_CATEGORIES:
        return "dos_or_ddos"
    return "other_attack"


def audit_file(path: Path, split: str, sample_values_limit: int = 20) -> tuple[dict, dict]:
    full_hashes: set[str] = set()
    model_feature_hashes: set[str] = set()
    pkseq_ids: set[str] = set()

    exact_duplicate_rows = 0
    duplicate_model_feature_rows = 0
    duplicate_pkseq = 0

    attack_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    subcategory_counts: Counter[str] = Counter()
    dos_scope_counts: Counter[str] = Counter()
    missing_counts: Counter[str] = Counter()
    type_counts: dict[str, Counter[str]] = defaultdict(Counter)
    unique_samples: dict[str, set[str]] = defaultdict(set)

    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"No header found in {path}")
        columns = reader.fieldnames
        model_feature_columns = [
            c for c in columns if c not in LABEL_COLUMNS and c not in ID_COLUMNS and c not in NETWORK_IDENTIFIER_COLUMNS
        ]
        rows = 0
        for row in reader:
            rows += 1
            values = [row.get(c, "") for c in columns]
            h = row_hash(values)
            if h in full_hashes:
                exact_duplicate_rows += 1
            else:
                full_hashes.add(h)

            model_values = [row.get(c, "") for c in model_feature_columns]
            mh = row_hash(model_values)
            if mh in model_feature_hashes:
                duplicate_model_feature_rows += 1
            else:
                model_feature_hashes.add(mh)

            pk = row.get("pkSeqID", "")
            if pk:
                if pk in pkseq_ids:
                    duplicate_pkseq += 1
                else:
                    pkseq_ids.add(pk)

            attack_counts[row.get("attack", "<missing>")] += 1
            category_counts[row.get("category", "<missing>")] += 1
            subcategory_counts[row.get("subcategory", "<missing>")] += 1
            dos_scope_counts[dos_scope_label(row)] += 1

            for col in columns:
                val = row.get(col, "")
                if is_missing(val):
                    missing_counts[col] += 1
                t = infer_type(val)
                type_counts[col][t] += 1
                if len(unique_samples[col]) < sample_values_limit and not is_missing(val):
                    unique_samples[col].add(val)

    column_profiles = []
    for col in columns:
        dominant_type = type_counts[col].most_common(1)[0][0] if type_counts[col] else "unknown"
        if col in LABEL_COLUMNS:
            role = "label"
        elif col in ID_COLUMNS:
            role = "identifier"
        elif col in NETWORK_IDENTIFIER_COLUMNS:
            role = "network_identifier"
        else:
            role = "candidate_feature"
        column_profiles.append(
            {
                "split": split,
                "column": col,
                "role": role,
                "dominant_type": dominant_type,
                "missing_count": missing_counts[col],
                "missing_rate": round(missing_counts[col] / rows, 8) if rows else 0,
                "sample_values": "; ".join(sorted(unique_samples[col])[:sample_values_limit]),
            }
        )

    file_summary = {
        "split": split,
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "rows": rows,
        "columns": len(columns),
        "column_names": columns,
        "exact_duplicate_rows": exact_duplicate_rows,
        "duplicate_pkseqid_rows": duplicate_pkseq,
        "duplicate_model_feature_rows_excluding_ids_labels": duplicate_model_feature_rows,
        "attack_counts": dict(attack_counts),
        "category_counts": dict(category_counts),
        "subcategory_counts": dict(subcategory_counts),
        "dos_scope_counts": dict(dos_scope_counts),
        "model_feature_columns_excluding_ids_labels": model_feature_columns,
        "high_leakage_or_excluded_columns": sorted(HIGH_LEAKAGE_COLUMNS & set(columns)),
    }

    sets = {
        "full_hashes": full_hashes,
        "model_feature_hashes": model_feature_hashes,
        "pkseq_ids": pkseq_ids,
    }
    return {"summary": file_summary, "column_profiles": column_profiles}, sets


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit BoT-IoT/UNSW-IoT CSV split files.")
    parser.add_argument("--data-dir", default="data/raw/bot-iot-hf", help="Directory containing train.csv/test.csv")
    parser.add_argument("--files", nargs="+", default=DEFAULT_FILES, help="CSV files to audit")
    parser.add_argument("--output-metrics", default="results/metrics/dataset_audit.json")
    parser.add_argument("--output-dir", default="results/tables")
    parser.add_argument("--source-name", default="Mireu-Lab/UNSW-IoT Hugging Face mirror")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)

    audits = []
    split_sets = {}
    for filename in args.files:
        path = data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset file: {path}")
        split = Path(filename).stem
        audit, sets = audit_file(path, split)
        audits.append(audit)
        split_sets[split] = sets

    split_leakage_checks = []
    if {"train", "test"}.issubset(split_sets):
        train = split_sets["train"]
        test = split_sets["test"]
        split_leakage_checks.extend(
            [
                {
                    "check": "pkSeqID overlap train/test",
                    "value": len(train["pkseq_ids"] & test["pkseq_ids"]),
                    "interpretation": "Should be 0 for clean split identifiers.",
                },
                {
                    "check": "Exact full-row overlap train/test",
                    "value": len(train["full_hashes"] & test["full_hashes"]),
                    "interpretation": "Should be 0 to avoid direct duplicate leakage.",
                },
                {
                    "check": "Model-feature signature overlap train/test excluding ids/network ids/labels",
                    "value": len(train["model_feature_hashes"] & test["model_feature_hashes"]),
                    "interpretation": "Non-zero can occur in aggregated flow features; high values mean random split similarity risk and should be disclosed.",
                },
            ]
        )

    file_rows = []
    class_rows = []
    column_rows = []
    for audit in audits:
        s = audit["summary"]
        file_rows.append(
            {
                "split": s["split"],
                "path": s["path"],
                "bytes": s["bytes"],
                "sha256": s["sha256"],
                "rows": s["rows"],
                "columns": s["columns"],
                "exact_duplicate_rows": s["exact_duplicate_rows"],
                "duplicate_pkseqid_rows": s["duplicate_pkseqid_rows"],
                "duplicate_model_feature_rows_excluding_ids_labels": s["duplicate_model_feature_rows_excluding_ids_labels"],
            }
        )
        for group_name in ["attack_counts", "category_counts", "subcategory_counts", "dos_scope_counts"]:
            for label, count in sorted(s[group_name].items()):
                class_rows.append(
                    {"split": s["split"], "group": group_name, "label": label, "count": count, "rate": round(count / s["rows"], 8)}
                )
        column_rows.extend(audit["column_profiles"])

    write_csv(
        output_dir / "dataset_files.csv",
        file_rows,
        ["split", "path", "bytes", "sha256", "rows", "columns", "exact_duplicate_rows", "duplicate_pkseqid_rows", "duplicate_model_feature_rows_excluding_ids_labels"],
    )
    write_csv(output_dir / "class_distribution.csv", class_rows, ["split", "group", "label", "count", "rate"])
    write_csv(output_dir / "column_profile.csv", column_rows, ["split", "column", "role", "dominant_type", "missing_count", "missing_rate", "sample_values"])
    write_csv(output_dir / "split_leakage_checks.csv", split_leakage_checks, ["check", "value", "interpretation"])

    metrics = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_name": args.source_name,
        "official_primary_source": "https://research.unsw.edu.au/projects/bot-iot-dataset",
        "working_mirror": "https://huggingface.co/datasets/Mireu-Lab/UNSW-IoT",
        "scope_decision": "Use inspected train/test CSV mirror for Fase 2 audit; cite UNSW BoT-IoT as primary dataset source. DoS/DDoS-vs-normal modeling should filter to normal and DoS/DDoS rows, excluding other attacks or treating them only in optional multiclass analysis.",
        "label_mapping": {
            "binary_attack": "attack=0 means normal; attack=1 means attack",
            "dos_scope": "category in {DoS, DDoS} -> dos_or_ddos; attack=0/category=Normal -> normal; other attack categories -> other_attack",
        },
        "recommended_excluded_columns_for_baseline": sorted(HIGH_LEAKAGE_COLUMNS),
        "recommended_candidate_features": audits[0]["summary"]["model_feature_columns_excluding_ids_labels"] if audits else [],
        "files": [audit["summary"] for audit in audits],
        "split_leakage_checks": split_leakage_checks,
        "outputs": {
            "dataset_files": str(output_dir / "dataset_files.csv"),
            "class_distribution": str(output_dir / "class_distribution.csv"),
            "column_profile": str(output_dir / "column_profile.csv"),
            "split_leakage_checks": str(output_dir / "split_leakage_checks.csv"),
        },
    }
    out = Path(args.output_metrics)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": True, "rows": {a["summary"]["split"]: a["summary"]["rows"] for a in audits}, "outputs": metrics["outputs"]}, indent=2))


if __name__ == "__main__":
    main()
