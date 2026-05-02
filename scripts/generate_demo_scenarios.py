#!/usr/bin/env python3
"""Generate Interactive SOC Replay demo data from committed artifacts.

This script intentionally creates small, sanitized JSON files for the dashboard.
It does not export raw datasets or model binaries.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
METRICS = ROOT / "results" / "metrics"
OUT = ROOT / "dashboard" / "data"
FEATURES = [
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
NUMERIC = [feature for feature in FEATURES if feature != "proto"]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def feature_payload(row: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for feature in FEATURES:
        if feature == "proto":
            payload[feature] = str(row.get(feature) or "tcp")
        else:
            payload[feature] = round(as_float(row.get(feature)), 6)
    return payload


def timeline(kind: str, outcome: str) -> list[dict[str, str]]:
    return [
        {
            "title": "Flow captured",
            "description": f"Satu flow trafik IoT dipilih untuk skenario {kind}; label/outcome demo: {outcome}.",
        },
        {
            "title": "Feature extraction",
            "description": "Backend membaca fitur agregat seperti connection count, packet rate, proto, dan statistik flow.",
        },
        {
            "title": "IDS decision",
            "description": "Model/surrogate menghitung risk score normal vs DoS/DDoS berdasarkan pola artifact.",
        },
        {
            "title": "SOC investigation",
            "description": "Analis SOC menyusun evidence chain, risiko FP/FN, dan rekomendasi mitigasi secara artifact-grounded.",
        },
    ]


def scenario_from_error(row: dict[str, str], index: int) -> dict[str, Any]:
    error_type = row.get("error_type", "error")
    is_fn = error_type.startswith("FN")
    name = "False Negative Attack Replay" if is_fn else "False Positive Normal Replay"
    description = (
        "Contoh attack DoS/DDoS yang terbaca normal oleh baseline; cocok untuk membahas risiko serangan lolos."
        if is_fn
        else "Contoh normal traffic yang terbaca attack oleh baseline; cocok untuk membahas beban alert analyst."
    )
    return {
        "id": f"artifact-{error_type.lower().replace('_', '-')}-{index}",
        "name": name,
        "description": description,
        "scenario_type": "artifact_error_case",
        "expected_outcome": error_type,
        "track": row.get("track"),
        "model": row.get("model"),
        "features": feature_payload(row),
        "timeline": timeline(name, error_type),
        "grounding": ["results/tables/forensic_error_examples.csv", "results/metrics/forensic_summary.json"],
    }


def synthetic_scenario(id_: str, name: str, description: str, outcome: str, features: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": id_,
        "name": name,
        "description": description,
        "scenario_type": "constructed_from_artifact_patterns",
        "expected_outcome": outcome,
        "track": "A_realistic_imbalanced",
        "model": "lightgbm_surrogate",
        "features": feature_payload(features),
        "timeline": timeline(name, outcome),
        "grounding": [
            "results/tables/advanced_shap_summary.csv",
            "results/tables/forensic_feature_importance.csv",
            "results/metrics/advanced_summary.json",
        ],
    }


def feature_ranges(error_examples: list[dict[str, str]]) -> dict[str, Any]:
    ranges: dict[str, Any] = {}
    for feature in NUMERIC:
        values = [as_float(row.get(feature)) for row in error_examples if row.get(feature) not in (None, "")]
        hi = max(values) if values else 10.0
        lo = min(values) if values else 0.0
        padded_hi = max(hi * 1.35, 1.0)
        ranges[feature] = {
            "min": 0,
            "max": round(padded_hi, 4),
            "step": 0.001 if padded_hi <= 5 else 0.01,
            "default": round((lo + hi) / 2, 4) if values else 0,
        }
    ranges["N_IN_Conn_P_DstIP"]["max"] = max(ranges["N_IN_Conn_P_DstIP"]["max"], 30)
    ranges["N_IN_Conn_P_SrcIP"]["max"] = max(ranges["N_IN_Conn_P_SrcIP"]["max"], 30)
    ranges["state_number"]["max"] = max(ranges["state_number"]["max"], 8)
    return {"generated_at_utc": now(), "features": ranges}


def top_evidence() -> list[dict[str, Any]]:
    shap = read_csv(TABLES / "advanced_shap_summary.csv")
    rows = [row for row in shap if row.get("track") == "A_realistic_imbalanced" and row.get("model") == "lightgbm"]
    return [
        {
            "rank": int(as_float(row.get("rank"))),
            "feature": row.get("feature"),
            "feature_group": row.get("feature_group"),
            "weight": as_float(row.get("normalized_mean_abs_shap")),
            "hint": row.get("interpretation_hint"),
        }
        for row in rows[:8]
    ]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    errors = read_csv(TABLES / "forensic_error_examples.csv")
    advanced = read_json(METRICS / "advanced_summary.json")
    fn = next((row for row in errors if row.get("track") == "A_realistic_imbalanced" and row.get("error_type", "").startswith("FN")), None)
    fp = next((row for row in errors if row.get("track") == "A_realistic_imbalanced" and row.get("error_type", "").startswith("FP")), None)
    scenarios: list[dict[str, Any]] = []
    if fn:
        scenarios.append(scenario_from_error(fn, 1))
    if fp:
        scenarios.append(scenario_from_error(fp, 1))
    scenarios.extend([
        synthetic_scenario(
            "simulated-high-confidence-dos",
            "Simulated High-risk DoS/DDoS Pattern",
            "Skenario edukatif yang dikonstruksi dari pola artifact: konsentrasi destination/source dan packet rate tinggi untuk menunjukkan alert yang mudah dijelaskan.",
            "educational_simulated_attack_pattern",
            {
                "proto": "udp",
                "stddev": 1.35,
                "N_IN_Conn_P_SrcIP": 22,
                "min": 0.02,
                "state_number": 4,
                "mean": 3.7,
                "N_IN_Conn_P_DstIP": 28,
                "drate": 0.18,
                "srate": 0.88,
                "max": 4.9,
            },
        ),
        synthetic_scenario(
            "simulated-low-risk-normal",
            "Simulated Low-risk Normal Pattern",
            "Skenario edukatif yang dikonstruksi dari pola artifact: trafik rendah risiko dengan concentration dan packet rate rendah sebagai pembanding baseline.",
            "educational_simulated_normal_pattern",
            {
                "proto": "tcp",
                "stddev": 0.08,
                "N_IN_Conn_P_SrcIP": 1,
                "min": 0.10,
                "state_number": 1,
                "mean": 0.18,
                "N_IN_Conn_P_DstIP": 1,
                "drate": 0.02,
                "srate": 0.03,
                "max": 0.4,
            },
        ),
    ])
    bundle = {
        "generated_at_utc": now(),
        "phase": "SOC Replay Edukatif",
        "status": "vps_backed_demo_primary_static_fallback",
        "metric_context": {
            "track_a_lightgbm_macro_f1": advanced.get("best_by_track", {}).get("A_realistic_imbalanced", {}).get("macro_f1"),
            "track_a_lightgbm_mcc": advanced.get("best_by_track", {}).get("A_realistic_imbalanced", {}).get("mcc"),
            "track_a_lightgbm_fp": advanced.get("best_by_track", {}).get("A_realistic_imbalanced", {}).get("fp"),
            "track_a_lightgbm_fn": advanced.get("best_by_track", {}).get("A_realistic_imbalanced", {}).get("fn"),
        },
        "top_evidence": top_evidence(),
        "scenarios": scenarios,
        "sources": [
            "results/tables/forensic_error_examples.csv",
            "results/tables/advanced_shap_summary.csv",
            "results/tables/forensic_feature_importance.csv",
            "results/metrics/advanced_summary.json",
        ],
        "claim_boundary": "Interactive prototype; artifact-grounded explanation; not production real-time IDS.",
    }
    (OUT / "demo-scenarios.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "demo-feature-ranges.json").write_text(json.dumps(feature_ranges(errors), indent=2, ensure_ascii=False), encoding="utf-8")
    templates = {
        "generated_at_utc": now(),
        "report_sections": ["summary", "evidence_chain", "risk_note", "recommendations", "limitation", "grounding"],
        "guardrail": "Only summarize evidence present in demo-scenarios.json and project artifacts.",
    }
    (OUT / "demo-narrative-templates.json").write_text(json.dumps(templates, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT / 'demo-scenarios.json'}")
    print(f"scenarios={len(scenarios)}")


if __name__ == "__main__":
    main()
