from __future__ import annotations

import csv
import importlib
import json
from pathlib import Path


def test_advanced_model_specs_and_skip_policy() -> None:
    module = importlib.import_module("scripts.run_advanced_modeling")
    assert set(module.ADVANCED_MODEL_SPECS) == {"lightgbm", "xgboost", "catboost"}
    assert module.should_skip("A_realistic_imbalanced", "xgboost", include_heavy_track_a=False) is True
    assert module.should_skip("A_realistic_imbalanced", "catboost", include_heavy_track_a=False) is True
    assert module.should_skip("A_realistic_imbalanced", "lightgbm", include_heavy_track_a=False) is False
    assert module.should_skip("A_realistic_imbalanced", "xgboost", include_heavy_track_a=True) is False


def test_advanced_feature_group_collapse() -> None:
    module = importlib.import_module("scripts.run_advanced_modeling")
    assert module.collapse_feature_name("proto=tcp") == "proto"
    assert module.collapse_feature_name("proto_udp") == "proto"
    assert module.collapse_feature_name("N_IN_Conn_P_DstIP") == "N_IN_Conn_P_DstIP"
    assert "target/gateway IoT" in module.FEATURE_INTERPRETATION["N_IN_Conn_P_DstIP"]


def test_advanced_reuses_leakage_safe_baseline_features() -> None:
    baseline = importlib.import_module("scripts.run_baseline_modeling")
    leakage_columns = {"attack", "category", "subcategory", "pkSeqID", "seq", "saddr", "sport", "daddr", "dport"}
    assert leakage_columns.isdisjoint(set(baseline.CANDIDATE_FEATURES))
    assert leakage_columns <= set(baseline.EXCLUDED_COLUMNS)


def test_advanced_summary_schema_if_present() -> None:
    summary_path = Path("results/metrics/advanced_summary.json")
    if not summary_path.exists():
        return
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["phase"] == "Fase 6A — Advanced/SOTA Modeling Extension"
    assert "best_overall_by_macro_f1_mcc" in summary
    assert "top_shap_feature_groups" in summary
    assert "limitations" in summary
    assert summary["metric_policy"].startswith("Advanced models must be compared")


def test_advanced_artifact_schema_if_present() -> None:
    metrics_path = Path("results/tables/advanced_model_metrics.csv")
    if not metrics_path.exists() or not metrics_path.read_text(encoding="utf-8").strip():
        return
    with metrics_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    required = {
        "track",
        "model",
        "macro_f1",
        "mcc",
        "recall_normal",
        "baseline_macro_f1_for_track",
        "delta_macro_f1_vs_baseline",
        "sample_limited",
    }
    assert rows
    assert required <= set(rows[0])


def test_advanced_shap_schema_if_present() -> None:
    shap_path = Path("results/tables/advanced_shap_summary.csv")
    if not shap_path.exists() or not shap_path.read_text(encoding="utf-8").strip():
        return
    with shap_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    required = {"track", "model", "method", "feature", "feature_group", "mean_abs_shap", "normalized_mean_abs_shap", "sample_rows"}
    assert rows
    assert required <= set(rows[0])
