from __future__ import annotations

from typing import Any

WEIGHTS = {
    "N_IN_Conn_P_DstIP": 0.30,
    "N_IN_Conn_P_SrcIP": 0.16,
    "srate": 0.14,
    "stddev": 0.12,
    "state_number": 0.10,
    "mean": 0.08,
    "max": 0.06,
    "drate": 0.04,
}
DENOMINATORS = {
    "N_IN_Conn_P_DstIP": 25,
    "N_IN_Conn_P_SrcIP": 25,
    "srate": 1,
    "drate": 1,
    "stddev": 1.6,
    "state_number": 6,
    "mean": 5,
    "max": 5,
}
REASONS = {
    "N_IN_Conn_P_DstIP": "konsentrasi koneksi ke destination IP/gateway IoT",
    "N_IN_Conn_P_SrcIP": "indikasi pola flood dari source tertentu",
    "srate": "source packet rate agresif",
    "drate": "ketidakseimbangan request-response",
    "stddev": "variasi flow abnormal",
    "state_number": "status koneksi abnormal/gagal",
    "mean": "intensitas umum trafik",
    "max": "spike maksimum trafik",
}
ALLOWED_FEATURES = set(WEIGHTS) | {"proto", "min"}
LEAKAGE_COLUMNS = {"attack", "category", "subcategory", "pkSeqID", "seq", "saddr", "sport", "daddr", "dport"}


def _number(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def validate_features(features: dict[str, Any]) -> None:
    leakage = sorted(set(features).intersection(LEAKAGE_COLUMNS))
    if leakage:
        raise ValueError(f"Rejected leakage/label columns: {', '.join(leakage)}")
    unknown = sorted(set(features) - ALLOWED_FEATURES)
    if unknown:
        raise ValueError(f"Unsupported feature columns: {', '.join(unknown)}")


def predict(features: dict[str, Any]) -> dict[str, Any]:
    validate_features(features)
    evidence = []
    for feature, weight in WEIGHTS.items():
        raw = _number(features.get(feature))
        normalized = _clamp(raw / DENOMINATORS.get(feature, 1))
        contribution = normalized * weight
        evidence.append(
            {
                "feature": feature,
                "value": raw,
                "weight": round(contribution, 6),
                "reason": REASONS.get(feature, "fitur pendukung"),
            }
        )
    proto = str(features.get("proto", "")).lower()
    proto_bonus = 0.04 if proto == "udp" else 0.025 if proto == "tcp" else 0.01
    risk_score = _clamp(sum(row["weight"] for row in evidence) + proto_bonus)
    label = "dos_or_ddos" if risk_score >= 0.55 else "normal"
    return {
        "label": label,
        "risk_score": round(risk_score, 6),
        "confidence": round(risk_score if label == "dos_or_ddos" else 1 - risk_score, 6),
        "threshold": 0.55,
        "model": "artifact-grounded surrogate IDS (server-side)",
        "evidence": sorted(evidence, key=lambda row: row["weight"], reverse=True)[:6],
    }
