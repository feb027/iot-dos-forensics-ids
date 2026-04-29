from __future__ import annotations

from typing import Any


def risk_level(score: float) -> str:
    if score >= 0.72:
        return "HIGH"
    if score >= 0.45:
        return "MEDIUM"
    return "LOW"


def build_report(scenario: dict[str, Any] | None, prediction: dict[str, Any], features: dict[str, Any]) -> dict[str, Any]:
    scenario_name = scenario.get("name") if scenario else "custom flow"
    expected = scenario.get("expected_outcome") if scenario else "unknown_custom_input"
    predicted = "DoS/DDoS" if prediction.get("label") == "dos_or_ddos" else "Normal"
    score = float(prediction.get("risk_score", 0))
    evidence_rows = prediction.get("evidence", [])[:5]
    evidence_chain = [
        f"{row.get('feature')}={row.get('value')} memberi kontribusi {row.get('weight')} karena {row.get('reason')}"
        for row in evidence_rows
    ]
    if not evidence_chain:
        evidence_chain = ["Tidak ada fitur dominan yang tersedia dari payload analisis."]
    if "FN" in str(expected):
        risk_note = "Skenario ini menonjolkan risiko false negative: attack dapat lolos sebagai normal, sehingga threshold dan evidence fitur perlu ditinjau."
    elif "FP" in str(expected):
        risk_note = "Skenario ini menonjolkan risiko false positive: trafik normal dapat membebani analyst sebagai alert palsu."
    else:
        risk_note = "Baca prediksi bersama confusion matrix, Track A realistic result, dan batasan normal class kecil."
    recs = [
        "Validasi concentration pada N_IN_Conn_P_DstIP dan N_IN_Conn_P_SrcIP sebelum eskalasi.",
        "Jika risk HIGH, prioritaskan rate limiting, traffic shaping, dan isolasi endpoint IoT target.",
        "Jika risk MEDIUM, lakukan monitoring ulang terhadap window trafik berikutnya untuk mengurangi FP/FN.",
        "Jangan gunakan output ini untuk attribution aktor; data hanya flow-level artifact BoT-IoT.",
    ]
    return {
        "source": "FastAPI deterministic SOC reporter",
        "summary": f"{scenario_name} dianalisis sebagai {predicted} dengan risk score {score:.3f} ({risk_level(score)}). Outcome demo: {expected}.",
        "evidence_chain": evidence_chain,
        "risk_note": risk_note,
        "recommendations": recs,
        "limitation": "Interactive prototype berbasis artifact eksperimen; bukan production real-time IDS dan bukan bukti attribution dunia nyata.",
        "grounding": (scenario or {}).get("grounding", ["dashboard/data/demo-scenarios.json", "dashboard/data/demo-feature-ranges.json"]),
        "features_used": {key: features.get(key) for key in sorted(features)},
    }
