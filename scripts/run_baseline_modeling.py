from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw" / "bot-iot-hf"
TRAIN_CSV = DATA_DIR / "train.csv"
TEST_CSV = DATA_DIR / "test.csv"
RESULTS_TABLES = ROOT / "results" / "tables"
RESULTS_FIGURES = ROOT / "results" / "figures"
RESULTS_METRICS = ROOT / "results" / "metrics"

RANDOM_STATE = 42
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
CATEGORICAL_FEATURES = ["proto"]
CANDIDATE_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
LABEL_COLUMNS = ["attack", "category", "subcategory"]
EXCLUDED_COLUMNS = [
    "attack",
    "category",
    "subcategory",
    "pkSeqID",
    "seq",
    "saddr",
    "sport",
    "daddr",
    "dport",
]
DOS_CATEGORIES = {"DoS", "DDoS"}
OTHER_ATTACK_CATEGORIES = {"Reconnaissance", "Theft"}

TRACKS = {
    "A_realistic_imbalanced": {
        "attack_multiplier": None,
        "description": "Realistic imbalanced split after excluding other_attack.",
    },
    "B_balanced_controlled_1_to_1": {
        "attack_multiplier": 1,
        "description": "Balanced controlled subset using all normal rows and equal sampled DoS/DDoS rows.",
    },
    "C_balanced_controlled_1_to_2": {
        "attack_multiplier": 2,
        "description": "Moderately imbalanced controlled subset using all normal rows and twice as many sampled DoS/DDoS rows.",
    },
}

MODEL_SPECS = {
    "dummy_majority": {
        "display_name": "Dummy Majority",
        "family": "sanity_baseline",
        "skip_tracks": set(),
    },
    "gaussian_nb": {
        "display_name": "Gaussian Naive Bayes",
        "family": "probabilistic_baseline",
        "skip_tracks": set(),
    },
    "sgd_logistic": {
        "display_name": "SGD Logistic Regression",
        "family": "linear_baseline",
        "skip_tracks": set(),
    },
    "decision_tree": {
        "display_name": "Decision Tree",
        "family": "tree_baseline",
        "skip_tracks": set(),
    },
    "random_forest": {
        "display_name": "Random Forest",
        "family": "ensemble_baseline",
        # Avoid training a full forest on 2.86M attack rows in the default run.
        # The controlled tracks still provide a tree-ensemble baseline.
        "skip_tracks": {"A_realistic_imbalanced"},
    },
}


@dataclass
class SplitData:
    frame: Any
    y: Any
    source_counts: dict[str, int]


def require_dependencies() -> None:
    missing: list[str] = []
    for module in ["pandas", "numpy", "sklearn", "matplotlib"]:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    if missing:
        raise SystemExit(
            "Missing ML dependencies: "
            + ", ".join(missing)
            + ". Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
        )


def classify_scope(category: str, attack: str) -> str:
    category = str(category)
    attack = str(attack)
    if attack in {"0", "0.0"} or category.lower() == "normal":
        return "normal"
    if category in DOS_CATEGORIES:
        return "dos_or_ddos"
    return "other_attack"


def read_split(path: Path, max_rows: int | None = None) -> Any:
    import pandas as pd

    usecols = CANDIDATE_FEATURES + LABEL_COLUMNS
    frame = pd.read_csv(path, usecols=usecols, nrows=max_rows)
    frame["scope"] = [classify_scope(c, a) for c, a in zip(frame["category"], frame["attack"])]
    return frame


def load_source_data(max_train_rows: int | None = None, max_test_rows: int | None = None) -> tuple[Any, Any]:
    if not TRAIN_CSV.exists() or not TEST_CSV.exists():
        raise FileNotFoundError(
            f"Expected cached BoT-IoT split CSVs under {DATA_DIR}. Missing train/test CSV."
        )
    train = read_split(TRAIN_CSV, max_train_rows)
    test = read_split(TEST_CSV, max_test_rows)
    return train, test


def validate_label_consistency(frame: Any, split: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    checks = {
        "attack_0_not_normal_category": ((frame["attack"].astype(str).isin(["0", "0.0"])) & (frame["category"].str.lower() != "normal")),
        "normal_category_not_attack_0": ((frame["category"].str.lower() == "normal") & (~frame["attack"].astype(str).isin(["0", "0.0"]))),
        "dos_ddos_category_not_attack_1": ((frame["category"].isin(DOS_CATEGORIES)) & (~frame["attack"].astype(str).isin(["1", "1.0"]))),
        "other_attack_category_wrong_scope": ((frame["category"].isin(OTHER_ATTACK_CATEGORIES)) & (frame["scope"] != "other_attack")),
    }
    for check, mask in checks.items():
        violations = int(mask.sum())
        rows.append({"split": split, "check": check, "violations": violations, "expected": 0, "status": "ok" if violations == 0 else "fail"})
    return rows


def build_track_split(frame: Any, track: str, split: str) -> SplitData:
    spec = TRACKS[track]
    binary = frame[frame["scope"].isin(["normal", "dos_or_ddos"])].copy()
    normal = binary[binary["scope"] == "normal"]
    attack = binary[binary["scope"] == "dos_or_ddos"]
    multiplier = spec["attack_multiplier"]
    if multiplier is None:
        selected = binary
        sampled_attack_rows = len(attack)
    else:
        sample_size = min(len(attack), len(normal) * int(multiplier))
        import pandas as pd

        selected_attack = attack.sample(n=sample_size, random_state=RANDOM_STATE, replace=False)
        selected = pd.concat([normal, selected_attack], axis=0).sample(frac=1.0, random_state=RANDOM_STATE).reset_index(drop=True)
        sampled_attack_rows = sample_size
    y = (selected["scope"] == "dos_or_ddos").astype(int)
    counts = {
        "normal_rows": int((selected["scope"] == "normal").sum()),
        "dos_or_ddos_rows": int((selected["scope"] == "dos_or_ddos").sum()),
        "sampled_dos_or_ddos_rows": int(sampled_attack_rows),
        "other_attack_rows_excluded": int((frame["scope"] == "other_attack").sum()),
        "total_rows": int(len(selected)),
    }
    return SplitData(frame=selected[CANDIDATE_FEATURES].copy(), y=y, source_counts=counts)


def make_preprocessor(model_name: str):
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    sparse = False
    if model_name == "gaussian_nb":
        numeric_transformer = "passthrough"
    else:
        numeric_transformer = StandardScaler()
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, NUMERIC_FEATURES),
            ("proto", OneHotEncoder(handle_unknown="ignore", sparse_output=sparse), CATEGORICAL_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def make_model(model_name: str):
    from sklearn.dummy import DummyClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import SGDClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.tree import DecisionTreeClassifier

    if model_name == "dummy_majority":
        return DummyClassifier(strategy="most_frequent")
    if model_name == "gaussian_nb":
        return GaussianNB()
    if model_name == "sgd_logistic":
        return SGDClassifier(
            loss="log_loss",
            class_weight="balanced",
            max_iter=2000,
            tol=1e-3,
            random_state=RANDOM_STATE,
        )
    if model_name == "decision_tree":
        return DecisionTreeClassifier(
            max_depth=8,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        )
    if model_name == "random_forest":
        return RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_leaf=3,
            class_weight="balanced_subsample",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
    raise ValueError(f"Unknown model: {model_name}")


def make_pipeline(model_name: str):
    from sklearn.pipeline import Pipeline

    return Pipeline([("preprocess", make_preprocessor(model_name)), ("model", make_model(model_name))])


def safe_div(num: float, den: float) -> float:
    return float(num / den) if den else 0.0


def evaluate_predictions(y_true: Any, y_pred: Any) -> dict[str, float | int]:
    from sklearn.metrics import (
        accuracy_score,
        balanced_accuracy_score,
        confusion_matrix,
        f1_score,
        matthews_corrcoef,
        precision_score,
        recall_score,
    )

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "precision_attack": float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "recall_attack": float(recall_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "f1_attack": float(f1_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "precision_normal": float(precision_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "recall_normal": float(recall_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "f1_normal": float(f1_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "false_positive_rate": safe_div(fp, fp + tn),
        "false_negative_rate": safe_div(fn, fn + tp),
    }


def selected_models(model_args: list[str]) -> list[str]:
    if not model_args or model_args == ["all"]:
        return list(MODEL_SPECS)
    unknown = sorted(set(model_args) - set(MODEL_SPECS))
    if unknown:
        raise ValueError(f"Unknown models: {unknown}")
    return model_args


def selected_tracks(track_args: list[str]) -> list[str]:
    if not track_args or track_args == ["all"]:
        return list(TRACKS)
    unknown = sorted(set(track_args) - set(TRACKS))
    if unknown:
        raise ValueError(f"Unknown tracks: {unknown}")
    return track_args


def run_experiments(args: argparse.Namespace) -> dict[str, Any]:
    require_dependencies()
    import pandas as pd

    RESULTS_TABLES.mkdir(parents=True, exist_ok=True)
    RESULTS_FIGURES.mkdir(parents=True, exist_ok=True)
    RESULTS_METRICS.mkdir(parents=True, exist_ok=True)

    train_source, test_source = load_source_data(args.max_train_rows, args.max_test_rows)
    label_checks = validate_label_consistency(train_source, "train") + validate_label_consistency(test_source, "test")
    if any(row["violations"] for row in label_checks):
        write_csv(RESULTS_TABLES / "baseline_label_consistency_checks.csv", label_checks)
        raise ValueError("Label consistency violations found before baseline modeling.")

    tracks = selected_tracks(args.tracks)
    models = selected_models(args.models)

    metrics_rows: list[dict[str, Any]] = []
    confusion_rows: list[dict[str, Any]] = []
    track_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []

    for track in tracks:
        train = build_track_split(train_source, track, "train")
        test = build_track_split(test_source, track, "test")
        track_rows.append({"track": track, "split": "train", **train.source_counts, "description": TRACKS[track]["description"]})
        track_rows.append({"track": track, "split": "test", **test.source_counts, "description": TRACKS[track]["description"]})

        for model_name in models:
            model_spec = MODEL_SPECS[model_name]
            if track in model_spec["skip_tracks"]:
                skipped_rows.append({
                    "track": track,
                    "model": model_name,
                    "reason": "Skipped by default to avoid excessive runtime on full imbalanced split; controlled tracks still run this model.",
                })
                continue
            pipeline = make_pipeline(model_name)
            start_fit = time.perf_counter()
            pipeline.fit(train.frame, train.y)
            fit_seconds = time.perf_counter() - start_fit
            start_pred = time.perf_counter()
            y_pred = pipeline.predict(test.frame)
            predict_seconds = time.perf_counter() - start_pred
            metrics = evaluate_predictions(test.y, y_pred)
            row = {
                "track": track,
                "model": model_name,
                "model_display_name": model_spec["display_name"],
                "model_family": model_spec["family"],
                "train_rows": train.source_counts["total_rows"],
                "train_normal_rows": train.source_counts["normal_rows"],
                "train_dos_or_ddos_rows": train.source_counts["dos_or_ddos_rows"],
                "test_rows": test.source_counts["total_rows"],
                "test_normal_rows": test.source_counts["normal_rows"],
                "test_dos_or_ddos_rows": test.source_counts["dos_or_ddos_rows"],
                "fit_seconds": round(fit_seconds, 4),
                "predict_seconds": round(predict_seconds, 4),
                "random_state": RANDOM_STATE,
                "sample_limited": bool(args.max_train_rows or args.max_test_rows),
                **{k: round(v, 8) if isinstance(v, float) else v for k, v in metrics.items()},
            }
            metrics_rows.append(row)
            confusion_rows.append({
                "track": track,
                "model": model_name,
                "tn_normal_correct": metrics["tn"],
                "fp_normal_as_attack": metrics["fp"],
                "fn_attack_as_normal": metrics["fn"],
                "tp_attack_correct": metrics["tp"],
            })
            print(json.dumps({"track": track, "model": model_name, "macro_f1": row["macro_f1"], "mcc": row["mcc"]}, ensure_ascii=False))

    write_csv(RESULTS_TABLES / "baseline_model_metrics.csv", metrics_rows)
    write_csv(RESULTS_TABLES / "baseline_confusion_matrices.csv", confusion_rows)
    write_csv(RESULTS_TABLES / "baseline_dataset_tracks.csv", track_rows)
    write_csv(RESULTS_TABLES / "baseline_label_consistency_checks.csv", label_checks)
    write_csv(RESULTS_TABLES / "baseline_skipped_runs.csv", skipped_rows)

    summary = build_summary(metrics_rows, track_rows, skipped_rows, args)
    (RESULTS_METRICS / "baseline_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    make_figures(metrics_rows, confusion_rows)
    return summary


def build_summary(metrics_rows: list[dict[str, Any]], track_rows: list[dict[str, Any]], skipped_rows: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    ranked = sorted(metrics_rows, key=lambda r: (r["macro_f1"], r["mcc"], r["recall_normal"]), reverse=True)
    best_by_track = {}
    for row in ranked:
        best_by_track.setdefault(row["track"], row)
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "Fase 4 — Baseline Modeling",
        "source_data_dir": str(DATA_DIR.relative_to(ROOT)),
        "target_definition": {
            "normal": 0,
            "dos_or_ddos": 1,
            "other_attack_policy": "excluded_from_primary_binary_baseline",
        },
        "candidate_features": CANDIDATE_FEATURES,
        "excluded_columns": EXCLUDED_COLUMNS,
        "tracks_requested": args.tracks,
        "models_requested": args.models,
        "random_state": RANDOM_STATE,
        "sample_limited": bool(args.max_train_rows or args.max_test_rows),
        "metric_policy": "Do not use accuracy as the primary claim; prioritize macro F1, MCC, balanced accuracy, recall_normal, recall_attack, confusion matrix, and FP/FN discussion.",
        "best_by_track": best_by_track,
        "best_overall_by_macro_f1_mcc": ranked[0] if ranked else None,
        "total_completed_runs": len(metrics_rows),
        "skipped_runs": skipped_rows,
        "outputs": {
            "tables": [
                "results/tables/baseline_model_metrics.csv",
                "results/tables/baseline_confusion_matrices.csv",
                "results/tables/baseline_dataset_tracks.csv",
                "results/tables/baseline_label_consistency_checks.csv",
                "results/tables/baseline_skipped_runs.csv",
            ],
            "figures": [
                "results/figures/baseline_macro_f1_comparison.png",
                "results/figures/baseline_mcc_comparison.png",
                "results/figures/baseline_confusion_matrix_grid.png",
            ],
        },
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def make_figures(metrics_rows: list[dict[str, Any]], confusion_rows: list[dict[str, Any]]) -> None:
    if not metrics_rows:
        return
    import math
    import matplotlib.pyplot as plt
    import pandas as pd

    metrics = pd.DataFrame(metrics_rows)
    for metric, filename, ylabel in [
        ("macro_f1", "baseline_macro_f1_comparison.png", "Macro F1"),
        ("mcc", "baseline_mcc_comparison.png", "Matthews Correlation Coefficient"),
    ]:
        fig, ax = plt.subplots(figsize=(13, 7))
        plot_df = metrics.sort_values(["track", metric], ascending=[True, False])
        labels = [f"{r.track}\n{r.model}" for r in plot_df.itertuples()]
        ax.bar(range(len(plot_df)), plot_df[metric].astype(float), color="#2563eb")
        ax.set_xticks(range(len(plot_df)))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(f"Fase 4 Baseline Comparison — {ylabel}")
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()
        fig.savefig(RESULTS_FIGURES / filename, dpi=180)
        plt.close(fig)

    confusion = pd.DataFrame(confusion_rows)
    n = len(confusion)
    cols = 3
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4.2, rows * 3.6))
    axes_flat = axes.ravel() if hasattr(axes, "ravel") else [axes]
    for ax, row in zip(axes_flat, confusion.itertuples()):
        matrix = [[row.tn_normal_correct, row.fp_normal_as_attack], [row.fn_attack_as_normal, row.tp_attack_correct]]
        im = ax.imshow(matrix, cmap="Blues")
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{matrix[i][j]:,}", ha="center", va="center", color="#111827")
        ax.set_xticks([0, 1], labels=["Pred Normal", "Pred DoS/DDoS"], fontsize=8)
        ax.set_yticks([0, 1], labels=["True Normal", "True DoS/DDoS"], fontsize=8)
        ax.set_title(f"{row.track}\n{row.model}", fontsize=9)
    for ax in axes_flat[n:]:
        ax.axis("off")
    fig.suptitle("Fase 4 Confusion Matrix Grid", y=1.02)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES / "baseline_confusion_matrix_grid.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Fase 4 baseline models for BoT-IoT DoS/DDoS detection.")
    parser.add_argument("--tracks", nargs="+", default=["all"], help=f"Tracks to run: all or {', '.join(TRACKS)}")
    parser.add_argument("--models", nargs="+", default=["all"], help=f"Models to run: all or {', '.join(MODEL_SPECS)}")
    parser.add_argument("--max-train-rows", type=int, default=None, help="Optional smoke-test limit for train CSV rows before filtering.")
    parser.add_argument("--max-test-rows", type=int, default=None, help="Optional smoke-test limit for test CSV rows before filtering.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_experiments(args)
    print(json.dumps({"ok": True, "completed_runs": summary["total_completed_runs"], "best": summary["best_overall_by_macro_f1_mcc"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
