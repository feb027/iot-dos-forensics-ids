from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.run_baseline_modeling as baseline

RESULTS_TABLES = ROOT / "results" / "tables"
RESULTS_FIGURES = ROOT / "results" / "figures"
RESULTS_METRICS = ROOT / "results" / "metrics"

ADVANCED_MODEL_SPECS: dict[str, dict[str, Any]] = {
    "lightgbm": {
        "display_name": "LightGBM Gradient Boosting",
        "family": "advanced_gradient_boosting",
        "package": "lightgbm",
        "skip_track_a_by_default": False,
        "forensic_note": "fast histogram gradient boosting for tabular network-flow IDS features",
    },
    "xgboost": {
        "display_name": "XGBoost Histogram Boosting",
        "family": "advanced_gradient_boosting",
        "package": "xgboost",
        "skip_track_a_by_default": True,
        "forensic_note": "strong tabular boosting baseline; Track A is skipped by default for memory/runtime control",
    },
    "catboost": {
        "display_name": "CatBoost Gradient Boosting",
        "family": "advanced_gradient_boosting",
        "package": "catboost",
        "skip_track_a_by_default": True,
        "forensic_note": "ordered boosting model included as a modern tabular comparison; Track A is skipped by default for memory/runtime control",
    },
}

ERROR_LABELS = {
    (0, 0): "TN_normal_correct",
    (0, 1): "FP_normal_as_attack",
    (1, 0): "FN_attack_as_normal",
    (1, 1): "TP_attack_correct",
}

FEATURE_INTERPRETATION = {
    "N_IN_Conn_P_DstIP": "jumlah koneksi masuk per destination IP; relevan untuk konsentrasi serangan ke target/gateway IoT",
    "N_IN_Conn_P_SrcIP": "jumlah koneksi masuk per source IP; membantu membaca pola flood dari sumber tertentu",
    "srate": "source packet rate; nilai tinggi dapat menunjukkan pengiriman paket agresif dari sumber serangan",
    "drate": "destination packet rate; membantu membaca ketidakseimbangan aliran request-response",
    "stddev": "deviasi statistik flow; membedakan stabilitas trafik normal dan variasi trafik serangan",
    "mean": "rata-rata statistik flow; merepresentasikan intensitas umum trafik",
    "max": "nilai maksimum statistik flow; menangkap spike intensitas trafik",
    "min": "nilai minimum statistik flow; mendukung pembacaan rentang trafik",
    "state_number": "kode status koneksi; membantu membaca pola koneksi gagal/abnormal",
    "proto": "protokol trafik; konteks transport/application layer untuk pola DoS/DDoS IoT",
}


@dataclass
class TrainedRun:
    track: str
    model_name: str
    pipeline: Any
    metrics: dict[str, Any]
    train_rows: int
    test_rows: int


def require_dependencies(models: list[str], shap_enabled: bool) -> None:
    missing: list[str] = []
    for module in ["pandas", "numpy", "sklearn", "matplotlib"]:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    for model_name in models:
        package = ADVANCED_MODEL_SPECS[model_name]["package"]
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    if shap_enabled:
        try:
            __import__("shap")
        except ImportError:
            missing.append("shap")
    if missing:
        raise SystemExit(
            "Missing advanced modeling dependencies: "
            + ", ".join(sorted(set(missing)))
            + ". Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
        )


def selected_models(model_args: list[str]) -> list[str]:
    if not model_args or model_args == ["all"]:
        return list(ADVANCED_MODEL_SPECS)
    unknown = sorted(set(model_args) - set(ADVANCED_MODEL_SPECS))
    if unknown:
        raise ValueError(f"Unknown advanced models: {unknown}")
    return model_args


def selected_tracks(track_args: list[str]) -> list[str]:
    return baseline.selected_tracks(track_args)


def should_skip(track: str, model_name: str, include_heavy_track_a: bool) -> bool:
    return bool(
        track == "A_realistic_imbalanced"
        and ADVANCED_MODEL_SPECS[model_name]["skip_track_a_by_default"]
        and not include_heavy_track_a
    )


def make_preprocessor():
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder

    return ColumnTransformer(
        transformers=[
            ("numeric", "passthrough", baseline.NUMERIC_FEATURES),
            ("proto", OneHotEncoder(handle_unknown="ignore", sparse_output=False), baseline.CATEGORICAL_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def make_model(model_name: str, args: argparse.Namespace):
    if model_name == "lightgbm":
        from lightgbm import LGBMClassifier

        return LGBMClassifier(
            n_estimators=args.n_estimators,
            learning_rate=args.learning_rate,
            num_leaves=31,
            max_depth=-1,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="binary",
            random_state=baseline.RANDOM_STATE,
            n_jobs=-1,
            verbosity=-1,
        )
    if model_name == "xgboost":
        from xgboost import XGBClassifier

        return XGBClassifier(
            n_estimators=args.n_estimators,
            learning_rate=args.learning_rate,
            max_depth=6,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="binary:logistic",
            eval_metric="logloss",
            tree_method="hist",
            random_state=baseline.RANDOM_STATE,
            n_jobs=-1,
        )
    if model_name == "catboost":
        from catboost import CatBoostClassifier

        return CatBoostClassifier(
            iterations=args.n_estimators,
            learning_rate=args.learning_rate,
            depth=6,
            loss_function="Logloss",
            random_seed=baseline.RANDOM_STATE,
            verbose=False,
            allow_writing_files=False,
            thread_count=-1,
        )
    raise ValueError(f"Unknown advanced model: {model_name}")


def make_pipeline(model_name: str, args: argparse.Namespace):
    from sklearn.pipeline import Pipeline

    return Pipeline([("preprocess", make_preprocessor()), ("model", make_model(model_name, args))])


def fit_pipeline(pipeline: Any, train_x: Any, train_y: Any) -> None:
    from sklearn.utils.class_weight import compute_sample_weight

    sample_weight = compute_sample_weight(class_weight="balanced", y=train_y)
    pipeline.fit(train_x, train_y, model__sample_weight=sample_weight)


def collapse_feature_name(feature: str) -> str:
    if feature.startswith("proto_") or feature.startswith("proto=") or feature.startswith("proto"):
        return "proto"
    return feature.split("=")[0]


def get_feature_names(pipeline: Any) -> list[str]:
    preprocessor = pipeline.named_steps["preprocess"]
    names = list(preprocessor.get_feature_names_out())
    clean: list[str] = []
    for name in names:
        clean.append(name.replace("proto_", "proto=") if name.startswith("proto_") else name)
    return clean


def extract_native_importance(run: TrainedRun) -> list[dict[str, Any]]:
    model = run.pipeline.named_steps["model"]
    feature_names = get_feature_names(run.pipeline)
    raw_importances = getattr(model, "feature_importances_", None)
    if raw_importances is None:
        return []
    values = [float(v) for v in raw_importances]
    total = sum(abs(v) for v in values) or 1.0
    rows = []
    for rank, idx in enumerate(sorted(range(len(values)), key=lambda i: abs(values[i]), reverse=True), start=1):
        feature = feature_names[idx]
        group = collapse_feature_name(feature)
        rows.append(
            {
                "track": run.track,
                "model": run.model_name,
                "method": "native_feature_importance",
                "rank": rank,
                "feature": feature,
                "feature_group": group,
                "importance": round(values[idx], 10),
                "normalized_importance": round(abs(values[idx]) / total, 10),
                "sample_rows": "",
                "interpretation_hint": FEATURE_INTERPRETATION.get(group, "fitur trafik pendukung interpretasi model"),
            }
        )
    return rows


def compute_shap_summary(run: TrainedRun, test_x: Any, sample_rows: int) -> list[dict[str, Any]]:
    import numpy as np
    import shap

    if sample_rows <= 0 or len(test_x) == 0:
        return []
    n = min(sample_rows, len(test_x))
    sample = test_x.sample(n=n, random_state=baseline.RANDOM_STATE) if hasattr(test_x, "sample") else test_x[:n]
    transformed = run.pipeline.named_steps["preprocess"].transform(sample)
    model = run.pipeline.named_steps["model"]
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(transformed)
    values = shap_values
    if isinstance(values, list):
        values = values[-1]
    values = np.asarray(values)
    if values.ndim == 3:
        values = values[:, :, -1]
    mean_abs = np.abs(values).mean(axis=0)
    feature_names = get_feature_names(run.pipeline)
    total = float(mean_abs.sum()) or 1.0
    rows = []
    for rank, idx in enumerate(np.argsort(-mean_abs), start=1):
        feature = feature_names[int(idx)]
        group = collapse_feature_name(feature)
        rows.append(
            {
                "track": run.track,
                "model": run.model_name,
                "method": "tree_shap_mean_abs",
                "rank": rank,
                "feature": feature,
                "feature_group": group,
                "mean_abs_shap": round(float(mean_abs[int(idx)]), 10),
                "normalized_mean_abs_shap": round(float(mean_abs[int(idx)]) / total, 10),
                "sample_rows": n,
                "interpretation_hint": FEATURE_INTERPRETATION.get(group, "fitur trafik pendukung interpretasi model"),
            }
        )
    return rows


def aggregate_feature_groups(rows: list[dict[str, Any]], value_key: str, output_key: str) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        group = row["feature_group"]
        entry = grouped.setdefault(
            group,
            {
                "feature_group": group,
                output_key: 0.0,
                "models": set(),
                "tracks": set(),
                "interpretation_hint": row.get("interpretation_hint", ""),
            },
        )
        entry[output_key] += float(row.get(value_key) or 0)
        entry["models"].add(row["model"])
        entry["tracks"].add(row["track"])
    ranked = sorted(grouped.values(), key=lambda r: r[output_key], reverse=True)
    total = sum(float(r[output_key]) for r in ranked) or 1.0
    out = []
    for rank, row in enumerate(ranked, start=1):
        out.append(
            {
                "rank": rank,
                "feature_group": row["feature_group"],
                output_key: round(float(row[output_key]), 10),
                "normalized": round(float(row[output_key]) / total, 10),
                "models": sorted(row["models"]),
                "tracks": sorted(row["tracks"]),
                "interpretation_hint": row.get("interpretation_hint", ""),
            }
        )
    return out


def load_baseline_best_by_track() -> dict[str, dict[str, Any]]:
    path = RESULTS_TABLES / "baseline_model_metrics.csv"
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_track: dict[str, dict[str, Any]] = {}
    for row in sorted(rows, key=lambda r: (float(r["macro_f1"]), float(r["mcc"]), float(r["recall_normal"])), reverse=True):
        by_track.setdefault(row["track"], row)
    return by_track


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    baseline.write_csv(path, rows)


def run_experiments(args: argparse.Namespace) -> dict[str, Any]:
    models = selected_models(args.models)
    tracks = selected_tracks(args.tracks)
    require_dependencies(models, shap_enabled=not args.skip_shap)

    RESULTS_TABLES.mkdir(parents=True, exist_ok=True)
    RESULTS_FIGURES.mkdir(parents=True, exist_ok=True)
    RESULTS_METRICS.mkdir(parents=True, exist_ok=True)

    train_source, test_source = baseline.load_source_data(args.max_train_rows, args.max_test_rows)
    label_checks = baseline.validate_label_consistency(train_source, "train") + baseline.validate_label_consistency(test_source, "test")
    if any(row["violations"] for row in label_checks):
        write_csv(RESULTS_TABLES / "advanced_label_consistency_checks.csv", label_checks)
        raise ValueError("Label consistency violations found before advanced modeling.")

    baseline_best = load_baseline_best_by_track()
    metric_rows: list[dict[str, Any]] = []
    confusion_rows: list[dict[str, Any]] = []
    importance_rows: list[dict[str, Any]] = []
    shap_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []
    trained_runs: list[TrainedRun] = []

    for track in tracks:
        train = baseline.build_track_split(train_source, track, "train")
        test = baseline.build_track_split(test_source, track, "test")
        for model_name in models:
            spec = ADVANCED_MODEL_SPECS[model_name]
            if should_skip(track, model_name, args.include_heavy_track_a):
                skipped_rows.append(
                    {
                        "track": track,
                        "model": model_name,
                        "reason": "Skipped by default to keep Track A memory/runtime controlled; rerun with --include-heavy-track-a if needed.",
                    }
                )
                continue
            pipeline = make_pipeline(model_name, args)
            start_fit = time.perf_counter()
            fit_pipeline(pipeline, train.frame, train.y)
            fit_seconds = time.perf_counter() - start_fit
            start_pred = time.perf_counter()
            y_pred = pipeline.predict(test.frame)
            predict_seconds = time.perf_counter() - start_pred
            metrics = baseline.evaluate_predictions(test.y, y_pred)
            base_row = baseline_best.get(track, {})
            baseline_macro_f1 = float(base_row.get("macro_f1") or 0)
            baseline_mcc = float(base_row.get("mcc") or 0)
            row = {
                "track": track,
                "model": model_name,
                "model_display_name": spec["display_name"],
                "model_family": spec["family"],
                "train_rows": train.source_counts["total_rows"],
                "train_normal_rows": train.source_counts["normal_rows"],
                "train_dos_or_ddos_rows": train.source_counts["dos_or_ddos_rows"],
                "test_rows": test.source_counts["total_rows"],
                "test_normal_rows": test.source_counts["normal_rows"],
                "test_dos_or_ddos_rows": test.source_counts["dos_or_ddos_rows"],
                "fit_seconds": round(fit_seconds, 4),
                "predict_seconds": round(predict_seconds, 4),
                "n_estimators": args.n_estimators,
                "learning_rate": args.learning_rate,
                "random_state": baseline.RANDOM_STATE,
                "sample_limited": bool(args.max_train_rows or args.max_test_rows),
                "baseline_best_model_for_track": base_row.get("model", ""),
                "baseline_macro_f1_for_track": round(baseline_macro_f1, 8),
                "baseline_mcc_for_track": round(baseline_mcc, 8),
                **{k: round(v, 8) if isinstance(v, float) else v for k, v in metrics.items()},
            }
            row["delta_macro_f1_vs_baseline"] = round(float(row["macro_f1"]) - baseline_macro_f1, 8)
            row["delta_mcc_vs_baseline"] = round(float(row["mcc"]) - baseline_mcc, 8)
            metric_rows.append(row)
            confusion_rows.append(
                {
                    "track": track,
                    "model": model_name,
                    "tn_normal_correct": metrics["tn"],
                    "fp_normal_as_attack": metrics["fp"],
                    "fn_attack_as_normal": metrics["fn"],
                    "tp_attack_correct": metrics["tp"],
                }
            )
            run = TrainedRun(track=track, model_name=model_name, pipeline=pipeline, metrics=metrics, train_rows=len(train.frame), test_rows=len(test.frame))
            trained_runs.append(run)
            importance_rows.extend(extract_native_importance(run))
            if not args.skip_shap:
                start_shap = time.perf_counter()
                shap_out = compute_shap_summary(run, test.frame, args.shap_sample)
                shap_seconds = round(time.perf_counter() - start_shap, 4)
                for shap_row in shap_out:
                    shap_row["shap_seconds_for_run"] = shap_seconds
                shap_rows.extend(shap_out)
            print(
                json.dumps(
                    {
                        "track": track,
                        "model": model_name,
                        "macro_f1": row["macro_f1"],
                        "mcc": row["mcc"],
                        "delta_macro_f1_vs_baseline": row["delta_macro_f1_vs_baseline"],
                    },
                    ensure_ascii=False,
                )
            )

    write_csv(RESULTS_TABLES / "advanced_model_metrics.csv", metric_rows)
    write_csv(RESULTS_TABLES / "advanced_confusion_matrices.csv", confusion_rows)
    write_csv(RESULTS_TABLES / "advanced_feature_importance.csv", importance_rows)
    write_csv(RESULTS_TABLES / "advanced_shap_summary.csv", shap_rows)
    write_csv(RESULTS_TABLES / "advanced_skipped_runs.csv", skipped_rows)
    write_csv(RESULTS_TABLES / "advanced_label_consistency_checks.csv", label_checks)

    summary = build_summary(metric_rows, importance_rows, shap_rows, skipped_rows, args)
    (RESULTS_METRICS / "advanced_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    make_figures(metric_rows, confusion_rows, shap_rows)
    return summary


def build_summary(
    metric_rows: list[dict[str, Any]],
    importance_rows: list[dict[str, Any]],
    shap_rows: list[dict[str, Any]],
    skipped_rows: list[dict[str, Any]],
    args: argparse.Namespace,
) -> dict[str, Any]:
    ranked = sorted(metric_rows, key=lambda r: (r["macro_f1"], r["mcc"], r["recall_normal"]), reverse=True)
    best_by_track = {}
    for row in ranked:
        best_by_track.setdefault(row["track"], row)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "Fase 6A — Advanced/SOTA Modeling Extension",
        "source_data_dir": str(baseline.DATA_DIR.relative_to(ROOT)),
        "target_definition": {
            "normal": 0,
            "dos_or_ddos": 1,
            "other_attack_policy": "excluded_from_primary_binary_advanced_modeling",
        },
        "candidate_features": baseline.CANDIDATE_FEATURES,
        "excluded_columns": baseline.EXCLUDED_COLUMNS,
        "tracks_requested": args.tracks,
        "models_requested": args.models,
        "models_available": ADVANCED_MODEL_SPECS,
        "random_state": baseline.RANDOM_STATE,
        "n_estimators": args.n_estimators,
        "learning_rate": args.learning_rate,
        "shap_sample": 0 if args.skip_shap else args.shap_sample,
        "sample_limited": bool(args.max_train_rows or args.max_test_rows),
        "metric_policy": "Advanced models must be compared against Fase 4 baselines using macro F1, MCC, recall, confusion matrix, FP/FN, and explainability; accuracy is not the primary claim.",
        "best_by_track": best_by_track,
        "best_overall_by_macro_f1_mcc": ranked[0] if ranked else None,
        "top_native_feature_groups": aggregate_feature_groups(importance_rows, "normalized_importance", "sum_normalized_importance")[:8],
        "top_shap_feature_groups": aggregate_feature_groups(shap_rows, "normalized_mean_abs_shap", "sum_normalized_mean_abs_shap")[:8],
        "total_completed_runs": len(metric_rows),
        "skipped_runs": skipped_rows,
        "limitations": [
            "Normal class remains tiny: advanced model scores must not be read as proof of perfect real-world detection.",
            "XGBoost and CatBoost skip full Track A by default unless --include-heavy-track-a is used, to keep local/WSL memory usage controlled.",
            "SHAP is computed on a bounded sample, so it supports forensic interpretation but is not a full-dataset explanation.",
            "Network identifiers and label columns remain excluded; interpretation focuses on aggregate traffic behavior, not host attribution.",
        ],
        "outputs": {
            "tables": [
                "results/tables/advanced_model_metrics.csv",
                "results/tables/advanced_confusion_matrices.csv",
                "results/tables/advanced_feature_importance.csv",
                "results/tables/advanced_shap_summary.csv",
                "results/tables/advanced_skipped_runs.csv",
            ],
            "figures": [
                "results/figures/advanced_macro_f1_vs_baseline.png",
                "results/figures/advanced_mcc_vs_baseline.png",
                "results/figures/advanced_confusion_matrix_grid.png",
                "results/figures/advanced_shap_summary.png",
            ],
        },
    }


def make_figures(metric_rows: list[dict[str, Any]], confusion_rows: list[dict[str, Any]], shap_rows: list[dict[str, Any]]) -> None:
    if not metric_rows:
        return
    import math
    import matplotlib.pyplot as plt
    import pandas as pd

    metrics = pd.DataFrame(metric_rows)
    for metric, baseline_metric, filename, ylabel in [
        ("macro_f1", "baseline_macro_f1_for_track", "advanced_macro_f1_vs_baseline.png", "Macro F1"),
        ("mcc", "baseline_mcc_for_track", "advanced_mcc_vs_baseline.png", "Matthews Correlation Coefficient"),
    ]:
        plot_df = metrics.sort_values(["track", metric], ascending=[True, False]).reset_index(drop=True)
        labels = [f"{r.track}\n{r.model}" for r in plot_df.itertuples()]
        x = range(len(plot_df))
        fig, ax = plt.subplots(figsize=(13, 7))
        ax.bar([i - 0.18 for i in x], plot_df[metric].astype(float), width=0.36, label="Advanced", color="#16a34a")
        ax.bar([i + 0.18 for i in x], plot_df[baseline_metric].astype(float), width=0.36, label="Best Fase 4 baseline on same track", color="#94a3b8")
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(f"Fase 6A Advanced Modeling vs Baseline — {ylabel}")
        ax.grid(axis="y", alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(RESULTS_FIGURES / filename, dpi=180)
        plt.close(fig)

    confusion = pd.DataFrame(confusion_rows)
    if not confusion.empty:
        n = len(confusion)
        cols = 3
        rows = math.ceil(n / cols)
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 4.2, rows * 3.6))
        axes_flat = axes.ravel() if hasattr(axes, "ravel") else [axes]
        for ax, row in zip(axes_flat, confusion.itertuples()):
            matrix = [[row.tn_normal_correct, row.fp_normal_as_attack], [row.fn_attack_as_normal, row.tp_attack_correct]]
            ax.imshow(matrix, cmap="Greens")
            for i in range(2):
                for j in range(2):
                    ax.text(j, i, f"{matrix[i][j]:,}", ha="center", va="center", color="#111827")
            ax.set_xticks([0, 1], labels=["Pred Normal", "Pred DoS/DDoS"], fontsize=8)
            ax.set_yticks([0, 1], labels=["True Normal", "True DoS/DDoS"], fontsize=8)
            ax.set_title(f"{row.track}\n{row.model}", fontsize=9)
        for ax in axes_flat[n:]:
            ax.axis("off")
        fig.suptitle("Fase 6A Advanced Confusion Matrix Grid", y=1.02)
        fig.tight_layout()
        fig.savefig(RESULTS_FIGURES / "advanced_confusion_matrix_grid.png", dpi=180, bbox_inches="tight")
        plt.close(fig)

    if shap_rows:
        shap_df = pd.DataFrame(shap_rows)
        grouped = shap_df.groupby("feature_group", as_index=False)["normalized_mean_abs_shap"].sum().sort_values("normalized_mean_abs_shap", ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(grouped["feature_group"][::-1], grouped["normalized_mean_abs_shap"][::-1], color="#7c3aed")
        ax.set_xlabel("Sum normalized mean |SHAP|")
        ax.set_title("Fase 6A SHAP Feature Group Summary")
        ax.grid(axis="x", alpha=0.25)
        fig.tight_layout()
        fig.savefig(RESULTS_FIGURES / "advanced_shap_summary.png", dpi=180)
        plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Fase 6A advanced/SOTA tabular models for BoT-IoT DoS/DDoS detection.")
    parser.add_argument("--tracks", nargs="+", default=["all"], help=f"Tracks to run: all or {', '.join(baseline.TRACKS)}")
    parser.add_argument("--models", nargs="+", default=["all"], help=f"Models to run: all or {', '.join(ADVANCED_MODEL_SPECS)}")
    parser.add_argument("--n-estimators", type=int, default=300, help="Boosting iterations/estimators.")
    parser.add_argument("--learning-rate", type=float, default=0.05, help="Boosting learning rate.")
    parser.add_argument("--shap-sample", type=int, default=3000, help="Rows per completed run for sampled SHAP explainability.")
    parser.add_argument("--skip-shap", action="store_true", help="Skip SHAP explainability.")
    parser.add_argument("--include-heavy-track-a", action="store_true", help="Also run XGBoost/CatBoost on full realistic Track A.")
    parser.add_argument("--max-train-rows", type=int, default=None, help="Optional smoke-test limit for train CSV rows before filtering.")
    parser.add_argument("--max-test-rows", type=int, default=None, help="Optional smoke-test limit for test CSV rows before filtering.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_experiments(args)
    print(json.dumps({"ok": True, "completed_runs": summary["total_completed_runs"], "best": summary["best_overall_by_macro_f1_mcc"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
