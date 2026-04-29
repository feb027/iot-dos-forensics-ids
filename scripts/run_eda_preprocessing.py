#!/usr/bin/env python3
"""Run Fase 3 EDA & preprocessing planning for BoT-IoT/UNSW-IoT CSV splits.

This script is intentionally lightweight: it streams the large CSV files and uses
only the Python standard library plus matplotlib for figures. It does not write
processed large datasets; it writes reproducible EDA tables, figures, and a JSON
preprocessing plan for the next modeling phase.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DEFAULT_FILES = ["train.csv", "test.csv"]
LABEL_COLUMNS = {"attack", "category", "subcategory"}
ID_COLUMNS = {"pkSeqID", "seq"}
NETWORK_IDENTIFIER_COLUMNS = {"saddr", "sport", "daddr", "dport"}
EXCLUDED_COLUMNS = LABEL_COLUMNS | ID_COLUMNS | NETWORK_IDENTIFIER_COLUMNS
CATEGORICAL_FEATURES = ["proto"]
NUMERIC_FEATURES = [
    "stddev",
    "N_IN_Conn_P_SrcIP",
    "min",
    "state_number",
    "mean",
    "N_IN_Conn_P_DstIP",
    "drate",
    "srate",
    "max",
]
CANDIDATE_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
DOS_CATEGORIES = {"DoS", "DDoS"}
RANDOM_STATE = 42


@dataclass
class OnlineStats:
    count: int = 0
    mean: float = 0.0
    m2: float = 0.0
    min_value: float | None = None
    max_value: float | None = None

    def update(self, value: float) -> None:
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self.m2 += delta * delta2
        self.min_value = value if self.min_value is None else min(self.min_value, value)
        self.max_value = value if self.max_value is None else max(self.max_value, value)

    @property
    def variance(self) -> float:
        return self.m2 / (self.count - 1) if self.count > 1 else 0.0

    @property
    def std(self) -> float:
        return math.sqrt(self.variance)


def is_missing(value: str) -> bool:
    return value == "" or value.lower() in {"na", "nan", "null", "none", "?"}


def to_float(value: str) -> float | None:
    if is_missing(value):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def dos_scope_label(row: dict[str, str]) -> str:
    attack = row.get("attack", "")
    category = row.get("category", "")
    if attack in {"0", "0.0"} or category.lower() == "normal":
        return "normal"
    if category in DOS_CATEGORIES:
        return "dos_or_ddos"
    return "other_attack"


def ensure_dirs(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pct(count: int, total: int) -> float:
    return round(count / total, 8) if total else 0.0


def audit_splits(data_dir: Path, files: list[str]) -> dict:
    split_rows: Counter[str] = Counter()
    category_counts: Counter[tuple[str, str]] = Counter()
    subcategory_counts: Counter[tuple[str, str]] = Counter()
    scope_counts: Counter[tuple[str, str]] = Counter()
    proto_scope_counts: Counter[tuple[str, str, str]] = Counter()
    label_consistency_violations: Counter[tuple[str, str]] = Counter()
    numeric_stats: dict[tuple[str, str, str], OnlineStats] = defaultdict(OnlineStats)
    missing_feature_counts: Counter[tuple[str, str]] = Counter()
    nonnumeric_counts: Counter[tuple[str, str]] = Counter()

    for filename in files:
        path = data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset file: {path}")
        split = Path(filename).stem
        with path.open(newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError(f"No header found in {path}")
            missing = [c for c in CANDIDATE_FEATURES + list(LABEL_COLUMNS) if c not in reader.fieldnames]
            if missing:
                raise ValueError(f"Missing expected columns in {path}: {missing}")
            for row in reader:
                split_rows[split] += 1
                scope = dos_scope_label(row)
                category = row.get("category", "<missing>")
                subcategory = row.get("subcategory", "<missing>")
                proto = row.get("proto", "<missing>")

                attack = row.get("attack", "")
                if attack in {"0", "0.0"} and category.lower() != "normal":
                    label_consistency_violations[(split, "attack_0_not_normal_category")] += 1
                if category.lower() == "normal" and attack not in {"0", "0.0"}:
                    label_consistency_violations[(split, "normal_category_not_attack_0")] += 1
                if category in DOS_CATEGORIES and attack not in {"1", "1.0"}:
                    label_consistency_violations[(split, "dos_ddos_category_not_attack_1")] += 1
                if category in {"Reconnaissance", "Theft"} and scope != "other_attack":
                    label_consistency_violations[(split, "other_attack_category_wrong_scope")] += 1

                category_counts[(split, category)] += 1
                subcategory_counts[(split, subcategory)] += 1
                scope_counts[(split, scope)] += 1
                proto_scope_counts[(split, scope, proto)] += 1

                for feature in NUMERIC_FEATURES:
                    raw = row.get(feature, "")
                    if is_missing(raw):
                        missing_feature_counts[(split, feature)] += 1
                        continue
                    value = to_float(raw)
                    if value is None:
                        nonnumeric_counts[(split, feature)] += 1
                        continue
                    numeric_stats[(split, scope, feature)].update(value)

    return {
        "split_rows": split_rows,
        "category_counts": category_counts,
        "subcategory_counts": subcategory_counts,
        "scope_counts": scope_counts,
        "proto_scope_counts": proto_scope_counts,
        "label_consistency_violations": label_consistency_violations,
        "numeric_stats": numeric_stats,
        "missing_feature_counts": missing_feature_counts,
        "nonnumeric_counts": nonnumeric_counts,
    }


def build_tables(audit: dict) -> dict[str, list[dict]]:
    split_rows: Counter[str] = audit["split_rows"]
    total_rows = sum(split_rows.values())

    category_rows = []
    for (split, category), count in sorted(audit["category_counts"].items()):
        category_rows.append(
            {"split": split, "category": category, "count": count, "rate": pct(count, split_rows[split])}
        )

    subcategory_rows = []
    for (split, subcategory), count in sorted(audit["subcategory_counts"].items()):
        subcategory_rows.append(
            {"split": split, "subcategory": subcategory, "count": count, "rate": pct(count, split_rows[split])}
        )

    scope_rows = []
    for (split, scope), count in sorted(audit["scope_counts"].items()):
        scope_rows.append({"split": split, "scope": scope, "count": count, "rate": pct(count, split_rows[split])})

    proto_rows = []
    for (split, scope, proto), count in sorted(audit["proto_scope_counts"].items()):
        denom = audit["scope_counts"][(split, scope)]
        proto_rows.append(
            {"split": split, "scope": scope, "proto": proto, "count": count, "rate_within_scope": pct(count, denom)}
        )

    label_consistency_rows = []
    label_checks = [
        "attack_0_not_normal_category",
        "normal_category_not_attack_0",
        "dos_ddos_category_not_attack_1",
        "other_attack_category_wrong_scope",
    ]
    for split in sorted(split_rows):
        for check in label_checks:
            label_consistency_rows.append(
                {
                    "split": split,
                    "check": check,
                    "violations": audit["label_consistency_violations"][(split, check)],
                    "expected": 0,
                    "status": "ok" if audit["label_consistency_violations"][(split, check)] == 0 else "fail",
                }
            )

    numeric_rows = []
    for (split, scope, feature), stats in sorted(audit["numeric_stats"].items()):
        numeric_rows.append(
            {
                "split": split,
                "scope": scope,
                "feature": feature,
                "count": stats.count,
                "mean": round(stats.mean, 8),
                "std": round(stats.std, 8),
                "min": stats.min_value,
                "max": stats.max_value,
                "missing_count": audit["missing_feature_counts"][(split, feature)],
                "nonnumeric_count": audit["nonnumeric_counts"][(split, feature)],
            }
        )

    feature_plan_rows = []
    for col in sorted(LABEL_COLUMNS):
        feature_plan_rows.append({"column": col, "role": "label", "phase3_action": "exclude_from_features"})
    for col in sorted(ID_COLUMNS):
        feature_plan_rows.append({"column": col, "role": "identifier", "phase3_action": "exclude_from_features"})
    for col in sorted(NETWORK_IDENTIFIER_COLUMNS):
        feature_plan_rows.append(
            {"column": col, "role": "network_identifier", "phase3_action": "exclude_from_features"}
        )
    for col in CATEGORICAL_FEATURES:
        feature_plan_rows.append({"column": col, "role": "categorical_feature", "phase3_action": "one_hot_encode"})
    for col in NUMERIC_FEATURES:
        feature_plan_rows.append({"column": col, "role": "numeric_feature", "phase3_action": "scale_or_passthrough"})

    dataset_plan_rows = []
    for split in sorted(split_rows):
        normal = audit["scope_counts"][(split, "normal")]
        dos = audit["scope_counts"][(split, "dos_or_ddos")]
        other = audit["scope_counts"][(split, "other_attack")]
        dataset_plan_rows.extend(
            [
                {
                    "track": "A_realistic_imbalanced",
                    "split": split,
                    "normal_rows": normal,
                    "dos_or_ddos_rows": dos,
                    "other_attack_rows": other,
                    "other_attack_policy": "exclude_from_binary_baseline",
                    "dos_sample_rows": dos,
                    "target_ratio_normal_to_dos": f"1:{round(dos / normal, 2) if normal else 'inf'}",
                    "random_state": "none",
                    "purpose": "Reflect audited distribution; evaluate with precision, recall, F1, confusion matrix, not accuracy alone.",
                },
                {
                    "track": "B_balanced_controlled_1_to_1",
                    "split": split,
                    "normal_rows": normal,
                    "dos_or_ddos_rows": dos,
                    "other_attack_rows": other,
                    "other_attack_policy": "exclude_from_binary_baseline",
                    "dos_sample_rows": min(dos, normal),
                    "target_ratio_normal_to_dos": "1:1",
                    "random_state": RANDOM_STATE,
                    "purpose": "Control imbalance so Fase 4 can test feature separability without majority-class dominance.",
                },
                {
                    "track": "C_balanced_controlled_1_to_2",
                    "split": split,
                    "normal_rows": normal,
                    "dos_or_ddos_rows": dos,
                    "other_attack_rows": other,
                    "other_attack_policy": "exclude_from_binary_baseline",
                    "dos_sample_rows": min(dos, normal * 2),
                    "target_ratio_normal_to_dos": "1:2",
                    "random_state": RANDOM_STATE,
                    "purpose": "Moderately imbalanced sensitivity check; still prevents millions of attacks from dominating.",
                },
            ]
        )

    return {
        "category": category_rows,
        "subcategory": subcategory_rows,
        "scope": scope_rows,
        "proto": proto_rows,
        "numeric": numeric_rows,
        "label_consistency": label_consistency_rows,
        "feature_plan": feature_plan_rows,
        "dataset_plan": dataset_plan_rows,
        "meta": [{"metric": "total_rows", "value": total_rows}],
    }


def plot_category_distribution(rows: list[dict], fig_path: Path) -> None:
    labels = sorted({r["category"] for r in rows})
    splits = sorted({r["split"] for r in rows})
    x = range(len(labels))
    width = 0.35
    plt.figure(figsize=(10, 5.5))
    for idx, split in enumerate(splits):
        counts = [next((r["count"] for r in rows if r["split"] == split and r["category"] == label), 0) for label in labels]
        offsets = [i + (idx - (len(splits) - 1) / 2) * width for i in x]
        plt.bar(offsets, counts, width=width, label=split)
    plt.yscale("log")
    plt.xticks(list(x), labels, rotation=30, ha="right")
    plt.ylabel("Row count (log scale)")
    plt.title("BoT-IoT Category Distribution by Split")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path, dpi=180)
    plt.close()


def plot_scope_distribution(rows: list[dict], fig_path: Path) -> None:
    labels = ["normal", "dos_or_ddos", "other_attack"]
    splits = sorted({r["split"] for r in rows})
    x = range(len(labels))
    width = 0.35
    plt.figure(figsize=(9, 5.2))
    for idx, split in enumerate(splits):
        counts = [next((r["count"] for r in rows if r["split"] == split and r["scope"] == label), 0) for label in labels]
        offsets = [i + (idx - (len(splits) - 1) / 2) * width for i in x]
        plt.bar(offsets, counts, width=width, label=split)
    plt.yscale("log")
    plt.xticks(list(x), labels)
    plt.ylabel("Row count (log scale)")
    plt.title("Binary Scope Distribution: Normal vs DoS/DDoS vs Other")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path, dpi=180)
    plt.close()


def plot_proto_by_scope(rows: list[dict], fig_path: Path) -> None:
    # Aggregate train+test for readability.
    counter: Counter[tuple[str, str]] = Counter()
    for row in rows:
        counter[(row["scope"], row["proto"])] += int(row["count"])
    scopes = ["normal", "dos_or_ddos", "other_attack"]
    protos = sorted({proto for _, proto in counter})
    bottom = [0] * len(scopes)
    plt.figure(figsize=(9, 5.2))
    for proto in protos:
        values = [counter[(scope, proto)] for scope in scopes]
        plt.bar(scopes, values, bottom=bottom, label=proto)
        bottom = [b + v for b, v in zip(bottom, values)]
    plt.yscale("log")
    plt.ylabel("Row count (log scale)")
    plt.title("Protocol Distribution by DoS Scope")
    plt.legend(title="proto")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=180)
    plt.close()


def plot_numeric_means(rows: list[dict], fig_path: Path) -> None:
    # Aggregate by scope across splits via weighted mean.
    aggregate: dict[tuple[str, str], tuple[float, int]] = {}
    for row in rows:
        scope = row["scope"]
        feature = row["feature"]
        if scope not in {"normal", "dos_or_ddos"}:
            continue
        count = int(row["count"])
        mean = float(row["mean"])
        prev_sum, prev_count = aggregate.get((scope, feature), (0.0, 0))
        aggregate[(scope, feature)] = (prev_sum + mean * count, prev_count + count)

    features = NUMERIC_FEATURES
    x = range(len(features))
    width = 0.35
    plt.figure(figsize=(12, 5.8))
    for idx, scope in enumerate(["normal", "dos_or_ddos"]):
        means = []
        for feature in features:
            total, count = aggregate.get((scope, feature), (0.0, 0))
            means.append(math.log10((total / count) + 1) if count else 0)
        offsets = [i + (idx - 0.5) * width for i in x]
        plt.bar(offsets, means, width=width, label=scope)
    plt.xticks(list(x), features, rotation=35, ha="right")
    plt.ylabel("log10(mean + 1)")
    plt.title("Numeric Feature Mean Comparison: Normal vs DoS/DDoS")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path, dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Fase 3 EDA and preprocessing planning for BoT-IoT CSV splits.")
    parser.add_argument("--data-dir", default="data/raw/bot-iot-hf", help="Directory containing train.csv/test.csv")
    parser.add_argument("--files", nargs="+", default=DEFAULT_FILES, help="CSV files to process")
    parser.add_argument("--tables-dir", default="results/tables")
    parser.add_argument("--figures-dir", default="results/figures")
    parser.add_argument("--metrics-path", default="results/metrics/preprocessing_summary.json")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    tables_dir = Path(args.tables_dir)
    figures_dir = Path(args.figures_dir)
    metrics_path = Path(args.metrics_path)
    ensure_dirs(tables_dir, figures_dir, metrics_path.parent)

    audit = audit_splits(data_dir, args.files)
    tables = build_tables(audit)

    write_csv(tables_dir / "eda_category_distribution.csv", tables["category"], ["split", "category", "count", "rate"])
    write_csv(
        tables_dir / "eda_subcategory_distribution.csv",
        tables["subcategory"],
        ["split", "subcategory", "count", "rate"],
    )
    write_csv(tables_dir / "eda_binary_scope_distribution.csv", tables["scope"], ["split", "scope", "count", "rate"])
    write_csv(
        tables_dir / "eda_protocol_distribution.csv",
        tables["proto"],
        ["split", "scope", "proto", "count", "rate_within_scope"],
    )
    write_csv(
        tables_dir / "eda_label_consistency_checks.csv",
        tables["label_consistency"],
        ["split", "check", "violations", "expected", "status"],
    )
    if any(int(row["violations"]) for row in tables["label_consistency"]):
        raise ValueError("Label consistency violations detected; inspect results/tables/eda_label_consistency_checks.csv")

    write_csv(
        tables_dir / "eda_numeric_feature_summary.csv",
        tables["numeric"],
        ["split", "scope", "feature", "count", "mean", "std", "min", "max", "missing_count", "nonnumeric_count"],
    )
    write_csv(tables_dir / "preprocessing_feature_plan.csv", tables["feature_plan"], ["column", "role", "phase3_action"])
    write_csv(
        tables_dir / "preprocessing_dataset_plan.csv",
        tables["dataset_plan"],
        [
            "track",
            "split",
            "normal_rows",
            "dos_or_ddos_rows",
            "other_attack_rows",
            "other_attack_policy",
            "dos_sample_rows",
            "target_ratio_normal_to_dos",
            "random_state",
            "purpose",
        ],
    )

    plot_category_distribution(tables["category"], figures_dir / "eda_category_distribution_log.png")
    plot_scope_distribution(tables["scope"], figures_dir / "eda_binary_scope_distribution_log.png")
    plot_proto_by_scope(tables["proto"], figures_dir / "eda_protocol_by_scope_log.png")
    plot_numeric_means(tables["numeric"], figures_dir / "eda_numeric_feature_means_log.png")

    split_rows = audit["split_rows"]
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_data_dir": str(data_dir),
        "files": args.files,
        "total_rows": sum(split_rows.values()),
        "split_rows": dict(split_rows),
        "candidate_features": CANDIDATE_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "excluded_columns": sorted(EXCLUDED_COLUMNS),
        "binary_target_definition": {
            "normal": "attack == 0 or category == Normal",
            "dos_or_ddos": "category in {DoS, DDoS}",
            "other_attack": "excluded from primary binary baseline, optional separate analysis",
        },
        "label_consistency_ok": all(int(row["violations"]) == 0 for row in tables["label_consistency"]),
        "label_consistency_checks": tables["label_consistency"],
        "recommended_phase4_tracks": [
            "A_realistic_imbalanced",
            "B_balanced_controlled_1_to_1",
            "C_balanced_controlled_1_to_2",
            "optional_DoS_vs_DDoS_or_protocol_subtype_forensic_analysis",
        ],
        "warnings": [
            "Normal class is extremely small; accuracy alone is not acceptable.",
            "Network identifiers and label columns must remain excluded from model features.",
            "Other attacks must not be silently mapped to normal in the primary binary task.",
            "Feature-signature similarity from Fase 2 should be disclosed when interpreting future model performance.",
        ],
        "outputs": {
            "tables": [
                "results/tables/eda_category_distribution.csv",
                "results/tables/eda_subcategory_distribution.csv",
                "results/tables/eda_binary_scope_distribution.csv",
                "results/tables/eda_protocol_distribution.csv",
                "results/tables/eda_numeric_feature_summary.csv",
                "results/tables/eda_label_consistency_checks.csv",
                "results/tables/preprocessing_feature_plan.csv",
                "results/tables/preprocessing_dataset_plan.csv",
            ],
            "figures": [
                "results/figures/eda_category_distribution_log.png",
                "results/figures/eda_binary_scope_distribution_log.png",
                "results/figures/eda_protocol_by_scope_log.png",
                "results/figures/eda_numeric_feature_means_log.png",
            ],
        },
    }
    metrics_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": True, "total_rows": summary["total_rows"], "outputs": summary["outputs"]}, indent=2))


if __name__ == "__main__":
    main()
