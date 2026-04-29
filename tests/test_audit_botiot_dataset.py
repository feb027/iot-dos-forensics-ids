from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
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
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_audit_botiot_dataset_outputs_expected_files(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    out_dir = tmp_path / "tables"
    metrics = tmp_path / "metrics.json"
    data_dir.mkdir()

    base = {
        "proto": "tcp",
        "saddr": "10.0.0.1",
        "sport": "1234",
        "daddr": "10.0.0.2",
        "dport": "80",
        "stddev": "0.1",
        "N_IN_Conn_P_SrcIP": "1",
        "min": "0.0",
        "state_number": "1",
        "mean": "0.1",
        "N_IN_Conn_P_DstIP": "1",
        "drate": "0.0",
        "srate": "1.0",
        "max": "0.2",
    }
    write_csv(
        data_dir / "train.csv",
        [
            {**base, "pkSeqID": "1", "seq": "10", "attack": "0", "category": "Normal", "subcategory": "Normal"},
            {**base, "pkSeqID": "2", "seq": "11", "attack": "1", "category": "DoS", "subcategory": "TCP"},
        ],
    )
    write_csv(
        data_dir / "test.csv",
        [
            {**base, "pkSeqID": "3", "seq": "12", "attack": "1", "category": "DDoS", "subcategory": "UDP"},
        ],
    )

    subprocess.run(
        [
            sys.executable,
            "scripts/audit_botiot_dataset.py",
            "--data-dir",
            str(data_dir),
            "--output-dir",
            str(out_dir),
            "--output-metrics",
            str(metrics),
        ],
        check=True,
        cwd=Path(__file__).resolve().parents[1],
    )

    assert (out_dir / "dataset_files.csv").exists()
    assert (out_dir / "class_distribution.csv").exists()
    assert (out_dir / "column_profile.csv").exists()
    assert (out_dir / "split_leakage_checks.csv").exists()
    data = json.loads(metrics.read_text(encoding="utf-8"))
    assert data["files"][0]["rows"] == 2
    assert data["files"][1]["rows"] == 1
    assert "attack" in data["recommended_excluded_columns_for_baseline"]
    assert "proto" in data["recommended_candidate_features"]
