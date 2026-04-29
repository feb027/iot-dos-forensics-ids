from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter
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

SELECTED_RUNS = [
    ("A_realistic_imbalanced", "decision_tree"),
    ("B_balanced_controlled_1_to_1", "decision_tree"),
    ("B_balanced_controlled_1_to_1", "random_forest"),
    ("C_balanced_controlled_1_to_2", "decision_tree"),
    ("C_balanced_controlled_1_to_2", "random_forest"),
]

ERROR_LABELS = {
    (0, 0): "TN_normal_correct",
    (0, 1): "FP_normal_as_attack",
    (1, 0): "FN_attack_as_normal",
    (1, 1): "TP_attack_correct",
}

FEATURE_INTERPRETATION = {
    "srate": "source packet rate; nilai tinggi dapat menunjukkan pengiriman paket agresif dari sumber serangan",
    "drate": "destination packet rate; perubahan tajam dapat menandai ketidakseimbangan aliran request-response",
    "N_IN_Conn_P_SrcIP": "jumlah koneksi masuk per source IP; nilai tinggi relevan untuk pola flood dari sumber tertentu",
    "N_IN_Conn_P_DstIP": "jumlah koneksi masuk per destination IP; nilai tinggi relevan untuk konsentrasi serangan ke target IoT",
    "state_number": "kode status koneksi; perubahan distribusi state membantu membaca pola koneksi gagal/abnormal",
    "stddev": "deviasi statistik flow; membantu membedakan kestabilan trafik normal dan variasi trafik serangan",
    "mean": "rata-rata statistik flow; dapat merepresentasikan intensitas umum trafik",
    "min": "nilai minimum statistik flow; membantu menangkap batas bawah pola trafik",
    "max": "nilai maksimum statistik flow; membantu menangkap spike intensitas trafik",
    "proto": "protokol trafik; membantu membaca kanal serangan yang dominan",
}


def build_track_frame(frame: Any, track: str) -> tuple[Any, Any, dict[str, int]]:
    import pandas as pd

    spec = baseline.TRACKS[track]
    binary = frame[frame["scope"].isin(["normal", "dos_or_ddos"])].copy()
    normal = binary[binary["scope"] == "normal"]
    attack = binary[binary["scope"] == "dos_or_ddos"]
    multiplier = spec["attack_multiplier"]
    if multiplier is None:
        selected = binary.reset_index(drop=True)
        sampled_attack_rows = len(attack)
    else:
        sample_size = min(len(attack), len(normal) * int(multiplier))
        selected_attack = attack.sample(n=sample_size, random_state=baseline.RANDOM_STATE, replace=False)
        selected = pd.concat([normal, selected_attack], axis=0).sample(frac=1.0, random_state=baseline.RANDOM_STATE).reset_index(drop=True)
        sampled_attack_rows = sample_size
    y = (selected["scope"] == "dos_or_ddos").astype(int)
    counts = {
        "normal_rows": int((selected["scope"] == "normal").sum()),
        "dos_or_ddos_rows": int((selected["scope"] == "dos_or_ddos").sum()),
        "sampled_dos_or_ddos_rows": int(sampled_attack_rows),
        "other_attack_rows_excluded": int((frame["scope"] == "other_attack").sum()),
        "total_rows": int(len(selected)),
    }
    return selected, y, counts


def get_transformed_feature_names(pipeline: Any) -> list[str]:
    preprocessor = pipeline.named_steps["preprocess"]
    names = list(preprocessor.get_feature_names_out())
    return [str(name).replace("proto_", "proto=") for name in names]


def collapse_feature_name(feature: str) -> str:
    if feature.startswith("proto="):
        return "proto"
    return feature


def model_importance_rows(track: str, model_name: str, pipeline: Any) -> list[dict[str, Any]]:
    model = pipeline.named_steps["model"]
    names = get_transformed_feature_names(pipeline)
    rows: list[dict[str, Any]] = []
    if hasattr(model, "feature_importances_"):
        values = list(model.feature_importances_)
        method = "tree_feature_importance"
    elif hasattr(model, "coef_"):
        values = [abs(float(v)) for v in model.coef_[0]]
        method = "absolute_linear_coefficient"
    else:
        return rows
    ranked = sorted(zip(names, values), key=lambda item: float(item[1]), reverse=True)
    total = sum(float(v) for _, v in ranked) or 1.0
    for rank, (feature, value) in enumerate(ranked, start=1):
        rows.append(
            {
                "track": track,
                "model": model_name,
                "method": method,
                "rank": rank,
                "feature": feature,
                "feature_group": collapse_feature_name(feature),
                "importance": round(float(value), 10),
                "normalized_importance": round(float(value) / total, 10),
                "interpretation_hint": FEATURE_INTERPRETATION.get(collapse_feature_name(feature), ""),
            }
        )
    return rows


def sample_for_permutation(frame: Any, y: Any, max_rows: int) -> tuple[Any, Any]:
    import pandas as pd

    tmp = frame[baseline.CANDIDATE_FEATURES + ["scope"]].copy()
    tmp["target"] = list(y)
    normal = tmp[tmp["target"] == 0]
    attack = tmp[tmp["target"] == 1]
    if len(tmp) <= max_rows:
        sampled = tmp
    else:
        normal_take = min(len(normal), max(1, max_rows // 4))
        attack_take = max_rows - normal_take
        sampled = pd.concat(
            [
                normal.sample(n=normal_take, random_state=baseline.RANDOM_STATE, replace=False),
                attack.sample(n=min(len(attack), attack_take), random_state=baseline.RANDOM_STATE, replace=False),
            ],
            axis=0,
        ).sample(frac=1.0, random_state=baseline.RANDOM_STATE)
    return sampled[baseline.CANDIDATE_FEATURES].copy(), sampled["target"].astype(int)


def permutation_importance_rows(track: str, model_name: str, pipeline: Any, test_frame: Any, y_test: Any, max_rows: int) -> list[dict[str, Any]]:
    from sklearn.inspection import permutation_importance

    sample_x, sample_y = sample_for_permutation(test_frame, y_test, max_rows)
    result = permutation_importance(
        pipeline,
        sample_x,
        sample_y,
        scoring="f1_macro",
        n_repeats=5,
        random_state=baseline.RANDOM_STATE,
        n_jobs=1,
    )
    ranked = sorted(
        zip(baseline.CANDIDATE_FEATURES, result.importances_mean, result.importances_std),
        key=lambda item: float(item[1]),
        reverse=True,
    )
    rows: list[dict[str, Any]] = []
    for rank, (feature, mean_value, std_value) in enumerate(ranked, start=1):
        rows.append(
            {
                "track": track,
                "model": model_name,
                "method": "permutation_macro_f1_drop",
                "rank": rank,
                "feature": feature,
                "feature_group": feature,
                "importance": round(float(mean_value), 10),
                "importance_std": round(float(std_value), 10),
                "sample_rows": int(len(sample_x)),
                "interpretation_hint": FEATURE_INTERPRETATION.get(feature, ""),
            }
        )
    return rows


def error_analysis_rows(track: str, model_name: str, test_frame: Any, y_true: Any, y_pred: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    example_rows: list[dict[str, Any]] = []
    working = test_frame.copy()
    working["y_true"] = list(y_true)
    working["y_pred"] = list(y_pred)
    working["error_type"] = [ERROR_LABELS[(int(t), int(p))] for t, p in zip(y_true, y_pred)]
    total = len(working) or 1
    for error_type, group in working.groupby("error_type", sort=True):
        proto_counts = Counter(group["proto"].astype(str)).most_common(3)
        category_counts = Counter(group["category"].astype(str)).most_common(3)
        row: dict[str, Any] = {
            "track": track,
            "model": model_name,
            "error_type": error_type,
            "count": int(len(group)),
            "rate_of_track_test": round(len(group) / total, 10),
            "top_proto": "; ".join(f"{label}:{count}" for label, count in proto_counts),
            "top_category": "; ".join(f"{label}:{count}" for label, count in category_counts),
        }
        for feature in baseline.NUMERIC_FEATURES:
            row[f"mean_{feature}"] = round(float(group[feature].mean()), 8) if len(group) else 0.0
        rows.append(row)
        if error_type.startswith(("FP_", "FN_")):
            for idx, sample in group.head(10).iterrows():
                example_rows.append(
                    {
                        "track": track,
                        "model": model_name,
                        "error_type": error_type,
                        "row_position_in_track_test": int(idx),
                        "proto": str(sample["proto"]),
                        "category": str(sample["category"]),
                        "subcategory": str(sample["subcategory"]),
                        **{feature: sample[feature] for feature in baseline.NUMERIC_FEATURES},
                    }
                )
    return rows, example_rows


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


def make_figures(feature_rows: list[dict[str, Any]], error_rows: list[dict[str, Any]]) -> None:
    if not feature_rows:
        return
    import matplotlib.pyplot as plt
    import pandas as pd

    RESULTS_FIGURES.mkdir(parents=True, exist_ok=True)
    feature_df = pd.DataFrame(feature_rows)
    model_df = feature_df[feature_df["method"].isin(["tree_feature_importance", "absolute_linear_coefficient"])]
    grouped = (
        model_df.groupby("feature_group", as_index=False)["normalized_importance"]
        .mean()
        .sort_values("normalized_importance", ascending=False)
        .head(12)
    )
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.barh(grouped["feature_group"][::-1], grouped["normalized_importance"][::-1], color="#2563eb")
    ax.set_xlabel("Mean normalized model importance")
    ax.set_title("Fase 5 Forensic Feature Importance — Aggregated Selected Models")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES / "forensic_feature_importance.png", dpi=180)
    plt.close(fig)

    if error_rows:
        error_df = pd.DataFrame(error_rows)
        pivot = error_df.pivot_table(index=["track", "model"], columns="error_type", values="count", aggfunc="sum", fill_value=0)
        wanted = ["FP_normal_as_attack", "FN_attack_as_normal"]
        for col in wanted:
            if col not in pivot.columns:
                pivot[col] = 0
        plot_df = pivot[wanted].reset_index()
        labels = [f"{r.track}\n{r.model}" for r in plot_df.itertuples()]
        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(plot_df))
        ax.bar(x, plot_df["FP_normal_as_attack"], label="FP normal→attack", color="#f97316")
        ax.bar(x, plot_df["FN_attack_as_normal"], bottom=plot_df["FP_normal_as_attack"], label="FN attack→normal", color="#dc2626")
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Error count")
        ax.set_title("Fase 5 Error Summary — False Positive and False Negative")
        ax.legend()
        ax.grid(axis="y", alpha=0.25)
        fig.tight_layout()
        fig.savefig(RESULTS_FIGURES / "forensic_confusion_error_summary.png", dpi=180)
        plt.close(fig)


def top_feature_groups(feature_rows: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for row in feature_rows:
        if row.get("method") not in {"tree_feature_importance", "absolute_linear_coefficient"}:
            continue
        group = row["feature_group"]
        totals[group] = totals.get(group, 0.0) + float(row.get("normalized_importance", 0.0))
        counts[group] = counts.get(group, 0) + 1
    ranked = sorted(((feature, totals[feature] / counts[feature]) for feature in totals), key=lambda item: item[1], reverse=True)
    return [
        {
            "rank": idx,
            "feature_group": feature,
            "mean_normalized_importance": round(value, 10),
            "interpretation_hint": FEATURE_INTERPRETATION.get(feature, ""),
        }
        for idx, (feature, value) in enumerate(ranked[:limit], start=1)
    ]


def build_summary(feature_rows: list[dict[str, Any]], error_rows: list[dict[str, Any]], example_rows: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    fp = sum(int(row["count"]) for row in error_rows if row["error_type"] == "FP_normal_as_attack")
    fn = sum(int(row["count"]) for row in error_rows if row["error_type"] == "FN_attack_as_normal")
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "phase": "Fase 5 — Forensic Analysis",
        "selected_runs": [{"track": track, "model": model} for track, model in SELECTED_RUNS],
        "top_feature_groups": top_feature_groups(feature_rows),
        "error_totals_selected_runs": {
            "false_positive_normal_as_attack": fp,
            "false_negative_attack_as_normal": fn,
            "error_examples_saved": len(example_rows),
        },
        "interpretation_policy": "Feature importance and FP/FN are interpreted as dataset-backed forensic evidence, not as proof of real-world perfect detection. Normal class is very small and split-similarity risk remains a limitation.",
        "limitations": [
            "Normal class is tiny: 370 train rows and 107 test rows in the audited split.",
            "Controlled Track B/C metrics can be high because attack rows are sampled around all available normal rows.",
            "Network identifiers and label columns remain excluded, so interpretation focuses on aggregate traffic features rather than attribution to specific IP/port evidence.",
            "Feature importance is model-dependent and should be read together with permutation importance and error analysis.",
        ],
        "sample_limited": bool(args.max_train_rows or args.max_test_rows),
        "outputs": {
            "tables": [
                "results/tables/forensic_feature_importance.csv",
                "results/tables/forensic_error_analysis.csv",
                "results/tables/forensic_error_examples.csv",
            ],
            "figures": [
                "results/figures/forensic_feature_importance.png",
                "results/figures/forensic_confusion_error_summary.png",
            ],
        },
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    baseline.require_dependencies()
    RESULTS_TABLES.mkdir(parents=True, exist_ok=True)
    RESULTS_FIGURES.mkdir(parents=True, exist_ok=True)
    RESULTS_METRICS.mkdir(parents=True, exist_ok=True)

    train_source, test_source = baseline.load_source_data(args.max_train_rows, args.max_test_rows)
    feature_rows: list[dict[str, Any]] = []
    error_rows: list[dict[str, Any]] = []
    example_rows: list[dict[str, Any]] = []

    for track, model_name in SELECTED_RUNS:
        if track in baseline.MODEL_SPECS[model_name]["skip_tracks"]:
            continue
        train_frame, y_train, train_counts = build_track_frame(train_source, track)
        test_frame, y_test, test_counts = build_track_frame(test_source, track)
        pipeline = baseline.make_pipeline(model_name)
        start = time.perf_counter()
        pipeline.fit(train_frame[baseline.CANDIDATE_FEATURES], y_train)
        y_pred = pipeline.predict(test_frame[baseline.CANDIDATE_FEATURES])
        elapsed = time.perf_counter() - start
        feature_rows.extend(model_importance_rows(track, model_name, pipeline))
        feature_rows.extend(permutation_importance_rows(track, model_name, pipeline, test_frame, y_test, args.permutation_max_rows))
        current_error_rows, current_examples = error_analysis_rows(track, model_name, test_frame, y_test, y_pred)
        for row in current_error_rows:
            row["train_rows"] = train_counts["total_rows"]
            row["test_rows"] = test_counts["total_rows"]
            row["fit_predict_seconds"] = round(elapsed, 4)
        error_rows.extend(current_error_rows)
        example_rows.extend(current_examples)
        print(json.dumps({"track": track, "model": model_name, "feature_rows": len(feature_rows), "error_rows": len(error_rows)}, ensure_ascii=False))

    write_csv(RESULTS_TABLES / "forensic_feature_importance.csv", feature_rows)
    write_csv(RESULTS_TABLES / "forensic_error_analysis.csv", error_rows)
    write_csv(RESULTS_TABLES / "forensic_error_examples.csv", example_rows)
    make_figures(feature_rows, error_rows)
    summary = build_summary(feature_rows, error_rows, example_rows, args)
    (RESULTS_METRICS / "forensic_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Fase 5 forensic analysis from baseline artifacts and retrained interpretable models.")
    parser.add_argument("--max-train-rows", type=int, default=None, help="Optional smoke-test row limit for train CSV before filtering.")
    parser.add_argument("--max-test-rows", type=int, default=None, help="Optional smoke-test row limit for test CSV before filtering.")
    parser.add_argument("--permutation-max-rows", type=int, default=5000, help="Max test rows used for permutation importance per selected run.")
    return parser.parse_args()


def main() -> None:
    summary = run(parse_args())
    print(json.dumps({"ok": True, "top_features": summary["top_feature_groups"][:5], "errors": summary["error_totals_selected_runs"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
