from __future__ import annotations

import csv
import importlib
import json
from pathlib import Path


def test_forensic_module_constants() -> None:
    module = importlib.import_module("scripts.run_forensic_analysis")
    assert ("A_realistic_imbalanced", "decision_tree") in module.SELECTED_RUNS
    assert ("B_balanced_controlled_1_to_1", "random_forest") in module.SELECTED_RUNS
    assert module.ERROR_LABELS[(0, 1)] == "FP_normal_as_attack"
    assert module.ERROR_LABELS[(1, 0)] == "FN_attack_as_normal"


def test_forensic_feature_group_collapse() -> None:
    module = importlib.import_module("scripts.run_forensic_analysis")
    assert module.collapse_feature_name("proto=tcp") == "proto"
    assert module.collapse_feature_name("srate") == "srate"
    assert "source packet rate" in module.FEATURE_INTERPRETATION["srate"]


def test_forensic_leakage_columns_excluded_from_candidate_features() -> None:
    baseline = importlib.import_module("scripts.run_baseline_modeling")
    leakage_columns = {"attack", "category", "subcategory", "pkSeqID", "seq", "saddr", "sport", "daddr", "dport"}
    assert leakage_columns.isdisjoint(set(baseline.CANDIDATE_FEATURES))
    assert leakage_columns <= set(baseline.EXCLUDED_COLUMNS)


def test_forensic_summary_schema_if_present() -> None:
    summary_path = Path("results/metrics/forensic_summary.json")
    if not summary_path.exists():
        return
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["phase"] == "Fase 5 — Forensic Analysis"
    assert "top_feature_groups" in summary
    assert "limitations" in summary
    assert "outputs" in summary
    assert summary["sample_limited"] is False


def test_forensic_artifact_schema_if_present() -> None:
    feature_path = Path("results/tables/forensic_feature_importance.csv")
    if not feature_path.exists() or not feature_path.read_text(encoding="utf-8").strip():
        return
    with feature_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    required = {"track", "model", "method", "rank", "feature", "feature_group", "importance"}
    assert rows
    assert required <= set(rows[0])


def test_forensic_permutation_importance_exists_for_selected_runs_if_present() -> None:
    feature_path = Path("results/tables/forensic_feature_importance.csv")
    if not feature_path.exists() or not feature_path.read_text(encoding="utf-8").strip():
        return
    module = importlib.import_module("scripts.run_forensic_analysis")
    with feature_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    permutation_runs = {(row["track"], row["model"]) for row in rows if row["method"] == "permutation_macro_f1_drop"}
    assert set(module.SELECTED_RUNS) <= permutation_runs


def test_forensic_error_analysis_matches_baseline_confusion_if_present() -> None:
    forensic_path = Path("results/tables/forensic_error_analysis.csv")
    baseline_path = Path("results/tables/baseline_confusion_matrices.csv")
    if not forensic_path.exists() or not baseline_path.exists():
        return
    if not forensic_path.read_text(encoding="utf-8").strip() or not baseline_path.read_text(encoding="utf-8").strip():
        return
    module = importlib.import_module("scripts.run_forensic_analysis")
    with forensic_path.open(newline="", encoding="utf-8") as f:
        forensic_rows = list(csv.DictReader(f))
    with baseline_path.open(newline="", encoding="utf-8") as f:
        baseline_rows = list(csv.DictReader(f))
    baseline_by_run = {(row["track"], row["model"]): row for row in baseline_rows}
    forensic_counts = {(row["track"], row["model"], row["error_type"]): int(row["count"]) for row in forensic_rows}
    mapping = {
        "TN_normal_correct": "tn_normal_correct",
        "FP_normal_as_attack": "fp_normal_as_attack",
        "FN_attack_as_normal": "fn_attack_as_normal",
        "TP_attack_correct": "tp_attack_correct",
    }
    for track, model in module.SELECTED_RUNS:
        baseline_row = baseline_by_run[(track, model)]
        for error_type, baseline_column in mapping.items():
            assert forensic_counts.get((track, model, error_type), 0) == int(baseline_row[baseline_column])
