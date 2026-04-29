from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

FIELDNAMES = [
    "pkSeqID",
    "proto",
    "saddr",
    "sport",
    "daddr",
    "dport",
    "seq",
    "stddev",
    "N_IN_Conn_P_SrcIP",
    "min",
    "state_number",
    "mean",
    "N_IN_Conn_P_DstIP",
    "drate",
    "srate",
    "max",
    "attack",
    "category",
    "subcategory",
]


def write_split(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def base_row(**overrides: str) -> dict[str, str]:
    row = {
        "pkSeqID": "1",
        "proto": "tcp",
        "saddr": "10.0.0.1",
        "sport": "1000",
        "daddr": "10.0.0.2",
        "dport": "80",
        "seq": "10",
        "stddev": "0.1",
        "N_IN_Conn_P_SrcIP": "1",
        "min": "0.0",
        "state_number": "1",
        "mean": "0.1",
        "N_IN_Conn_P_DstIP": "1",
        "drate": "0.0",
        "srate": "1.0",
        "max": "0.2",
        "attack": "0",
        "category": "Normal",
        "subcategory": "Normal",
    }
    row.update(overrides)
    return row


def test_run_eda_preprocessing_creates_tables_figures_and_plan(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    tables_dir = tmp_path / "tables"
    figures_dir = tmp_path / "figures"
    metrics_path = tmp_path / "metrics" / "preprocessing_summary.json"
    data_dir.mkdir()

    write_split(
        data_dir / "train.csv",
        [
            base_row(pkSeqID="1", attack="0", category="Normal", subcategory="Normal", proto="tcp"),
            base_row(pkSeqID="2", attack="1", category="DoS", subcategory="TCP", proto="tcp"),
            base_row(pkSeqID="3", attack="1", category="DDoS", subcategory="UDP", proto="udp"),
            base_row(pkSeqID="4", attack="1", category="Reconnaissance", subcategory="Service_Scan", proto="tcp"),
        ],
    )
    write_split(
        data_dir / "test.csv",
        [
            base_row(pkSeqID="5", attack="0", category="Normal", subcategory="Normal", proto="tcp"),
            base_row(pkSeqID="6", attack="1", category="DoS", subcategory="UDP", proto="udp"),
        ],
    )

    subprocess.run(
        [
            sys.executable,
            "scripts/run_eda_preprocessing.py",
            "--data-dir",
            str(data_dir),
            "--tables-dir",
            str(tables_dir),
            "--figures-dir",
            str(figures_dir),
            "--metrics-path",
            str(metrics_path),
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
    )

    assert (tables_dir / "eda_binary_scope_distribution.csv").exists()
    assert (tables_dir / "eda_label_consistency_checks.csv").exists()
    assert (tables_dir / "preprocessing_feature_plan.csv").exists()
    assert (tables_dir / "preprocessing_dataset_plan.csv").exists()
    assert (figures_dir / "eda_binary_scope_distribution_log.png").exists()
    summary = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert summary["total_rows"] == 6
    assert summary["label_consistency_ok"] is True
    assert "proto" in summary["categorical_features"]
    assert "attack" in summary["excluded_columns"]
    assert "B_balanced_controlled_1_to_1" in summary["recommended_phase4_tracks"]
    assert "C_balanced_controlled_1_to_2" in summary["recommended_phase4_tracks"]

    with (tables_dir / "eda_binary_scope_distribution.csv").open(newline="", encoding="utf-8") as f:
        scope_rows = {(r["split"], r["scope"]): int(r["count"]) for r in csv.DictReader(f)}
    assert scope_rows[("train", "normal")] == 1
    assert scope_rows[("train", "dos_or_ddos")] == 2
    assert scope_rows[("train", "other_attack")] == 1
    assert scope_rows[("test", "normal")] == 1
    assert scope_rows[("test", "dos_or_ddos")] == 1

    with (tables_dir / "preprocessing_feature_plan.csv").open(newline="", encoding="utf-8") as f:
        feature_actions = {r["column"]: r["phase3_action"] for r in csv.DictReader(f)}
    for excluded in ["attack", "category", "subcategory", "pkSeqID", "seq", "saddr", "sport", "daddr", "dport"]:
        assert feature_actions[excluded] == "exclude_from_features"

    with (tables_dir / "preprocessing_dataset_plan.csv").open(newline="", encoding="utf-8") as f:
        plan_rows = list(csv.DictReader(f))
    tracks = {r["track"] for r in plan_rows}
    assert {"A_realistic_imbalanced", "B_balanced_controlled_1_to_1", "C_balanced_controlled_1_to_2"} <= tracks
    assert all(r["other_attack_policy"] == "exclude_from_binary_baseline" for r in plan_rows)
