import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generate_demo_scenarios_outputs_valid_json():
    result = subprocess.run(
        [sys.executable, "scripts/generate_demo_scenarios.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "scenarios=" in result.stdout
    scenarios = json.loads((ROOT / "dashboard/data/demo-scenarios.json").read_text())
    ranges = json.loads((ROOT / "dashboard/data/demo-feature-ranges.json").read_text())
    assert scenarios["phase"] == "Fase 6B — Interactive AI SOC Demo"
    assert len(scenarios["scenarios"]) >= 4
    assert "N_IN_Conn_P_DstIP" in ranges["features"]
    assert scenarios["claim_boundary"].startswith("Interactive prototype")


def test_predictor_rejects_leakage_columns_and_scores_high_risk():
    sys.path.insert(0, str(ROOT / "backend"))
    from iot_soc_api.predictor import predict

    high = predict(
        {
            "proto": "udp",
            "N_IN_Conn_P_DstIP": 28,
            "N_IN_Conn_P_SrcIP": 22,
            "srate": 0.88,
            "drate": 0.18,
            "stddev": 1.35,
            "state_number": 4,
            "mean": 3.7,
            "max": 4.9,
            "min": 0.02,
        }
    )
    assert high["label"] == "dos_or_ddos"
    assert high["risk_score"] > 0.55

    try:
        predict({"attack": 1, "N_IN_Conn_P_DstIP": 1})
    except ValueError as exc:
        assert "Rejected leakage" in str(exc)
    else:
        raise AssertionError("leakage column was accepted")


def test_fastapi_health_and_soc_report():
    sys.path.insert(0, str(ROOT / "backend"))
    from fastapi.testclient import TestClient
    from iot_soc_api.app import create_app

    client = TestClient(create_app())
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["scenarios"] >= 4

    payload = {
        "scenario_id": "simulated-high-confidence-dos",
        "features": {
            "proto": "udp",
            "N_IN_Conn_P_DstIP": 28,
            "N_IN_Conn_P_SrcIP": 22,
            "srate": 0.88,
            "drate": 0.18,
            "stddev": 1.35,
            "state_number": 4,
            "mean": 3.7,
            "max": 4.9,
            "min": 0.02,
        },
    }
    prediction = client.post("/api/predict", json=payload)
    assert prediction.status_code == 200
    assert prediction.json()["label"] == "dos_or_ddos"

    report = client.post("/api/soc/analyze", json={**payload, "prediction": prediction.json()})
    assert report.status_code == 200
    body = report.json()
    assert "risk score" in body["summary"]
    assert body["recommendations"]
