from __future__ import annotations

import csv
import importlib
from pathlib import Path


def test_baseline_module_imports_without_ml_dependencies() -> None:
    module = importlib.import_module("scripts.run_baseline_modeling")
    assert module.CANDIDATE_FEATURES == [
        "proto",
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
    assert set(module.EXCLUDED_COLUMNS) == {
        "attack",
        "category",
        "subcategory",
        "pkSeqID",
        "seq",
        "saddr",
        "sport",
        "daddr",
        "dport",
    }


def test_baseline_scope_mapping() -> None:
    module = importlib.import_module("scripts.run_baseline_modeling")
    assert module.classify_scope("Normal", "0") == "normal"
    assert module.classify_scope("DoS", "1") == "dos_or_ddos"
    assert module.classify_scope("DDoS", "1") == "dos_or_ddos"
    assert module.classify_scope("Reconnaissance", "1") == "other_attack"
    assert module.classify_scope("Theft", "1") == "other_attack"


def test_baseline_tracks_and_models_are_declared() -> None:
    module = importlib.import_module("scripts.run_baseline_modeling")
    assert {
        "A_realistic_imbalanced",
        "B_balanced_controlled_1_to_1",
        "C_balanced_controlled_1_to_2",
    } <= set(module.TRACKS)
    assert {"gaussian_nb", "sgd_logistic", "decision_tree"} <= set(module.MODEL_SPECS)
    assert "A_realistic_imbalanced" in module.MODEL_SPECS["random_forest"]["skip_tracks"]


def test_baseline_artifact_schema_if_present() -> None:
    metrics_path = Path("results/tables/baseline_model_metrics.csv")
    if not metrics_path.exists() or not metrics_path.read_text(encoding="utf-8").strip():
        return
    with metrics_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    required = {
        "track",
        "model",
        "macro_f1",
        "mcc",
        "balanced_accuracy",
        "precision_attack",
        "recall_attack",
        "precision_normal",
        "recall_normal",
        "tn",
        "fp",
        "fn",
        "tp",
    }
    assert rows
    assert required <= set(rows[0])
