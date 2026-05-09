from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_scaffold_files_exist() -> None:
    required = [
        "README.md",
        "docs/dataset-notes.md",
        "references/literature-matrix.md",
        "references/references.bib",
        "dashboard/index.html",
        "dashboard/app.js",
        "dashboard/data/dashboard-data.json",
        "scripts/generate_dashboard_data.py",
        "scripts/run_eda_preprocessing.py",
        "notebooks/01_eda_preprocessing.ipynb",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    assert not missing


def test_dashboard_data_contract_is_valid_json() -> None:
    data_path = ROOT / "dashboard" / "data" / "dashboard-data.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    for key in [
        "project",
        "dataset_summary",
        "class_distribution",
        "eda_summary",
        "model_comparison",
        "confusion_matrix",
        "feature_importance",
        "forensic_notes",
    ]:
        assert key in data
    assert data["project"]["primary_dataset"] == "BoT-IoT (UNSW)"


def test_dashboard_data_generator_runs_and_preserves_contract() -> None:
    import subprocess
    import sys

    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_dashboard_data.py")], check=True, cwd=ROOT)
    data = json.loads((ROOT / "dashboard" / "data" / "dashboard-data.json").read_text(encoding="utf-8"))
    assert data["project"]["title"] == "Sistem Analisis Serangan DoS pada Arsitektur IoT"
    assert isinstance(data["class_distribution"], list)
    assert isinstance(data["eda_summary"], dict)
    assert isinstance(data["model_comparison"], list)
    assert isinstance(data["feature_importance"], list)
