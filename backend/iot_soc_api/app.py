from __future__ import annotations

import csv
import io
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .artifacts import find_scenario, load_demo_bundle
from .predictor import LEAKAGE_COLUMNS, predict, validate_features
from .reporter import build_report


class PredictRequest(BaseModel):
    features: dict[str, Any] = Field(default_factory=dict)
    scenario_id: str | None = None


class SocAnalyzeRequest(BaseModel):
    scenario_id: str | None = None
    features: dict[str, Any] = Field(default_factory=dict)
    prediction: dict[str, Any] | None = None


class FlowAnalyzeRequest(BaseModel):
    csv_text: str


class ChatRequest(BaseModel):
    question: str


def create_app() -> FastAPI:
    app = FastAPI(title="IoT DoS AI SOC Demo API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        bundle = load_demo_bundle()
        return {
            "service": "iot-dos-ai-soc-demo",
            "mode": "vps-backed deterministic artifact-grounded",
            "scenarios": len(bundle.get("scenarios", [])),
            "claim_boundary": bundle.get("claim_boundary"),
        }

    @app.get("/api/scenarios")
    def scenarios() -> dict[str, Any]:
        return load_demo_bundle()

    @app.post("/api/predict")
    def predict_endpoint(request: PredictRequest) -> dict[str, Any]:
        try:
            return predict(request.features)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/api/soc/analyze")
    def soc_analyze(request: SocAnalyzeRequest) -> dict[str, Any]:
        scenario = find_scenario(request.scenario_id)
        try:
            prediction = request.prediction or predict(request.features)
            validate_features(request.features)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return build_report(scenario, prediction, request.features)

    @app.post("/api/flow/analyze")
    def flow_analyze(request: FlowAnalyzeRequest) -> dict[str, Any]:
        try:
            rows = list(csv.DictReader(io.StringIO(request.csv_text.strip())))
        except csv.Error as exc:
            raise HTTPException(status_code=400, detail=f"Invalid CSV: {exc}") from exc
        if not rows:
            raise HTTPException(status_code=400, detail="CSV must include header and one data row")
        row = rows[0]
        leakage = sorted(set(row).intersection(LEAKAGE_COLUMNS))
        if leakage:
            raise HTTPException(status_code=400, detail=f"Rejected leakage/label columns: {', '.join(leakage)}")
        features = {key: value for key, value in row.items() if value not in (None, "")}
        try:
            prediction = predict(features)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"prediction": prediction, "report": build_report(None, prediction, features)}

    @app.post("/api/chat")
    def chat(request: ChatRequest) -> dict[str, Any]:
        q = request.question.lower()
        bundle = load_demo_bundle()
        if "accuracy" in q or "akurasi" in q:
            answer = "Accuracy tidak dijadikan klaim utama karena normal class sangat kecil; dashboard memakai macro F1, MCC, confusion matrix, dan FP/FN."
        elif "track a" in q:
            ctx = bundle.get("metric_context", {})
            answer = f"Track A realistic adalah distribusi paling dekat audit asli. LightGBM Track A macro F1={ctx.get('track_a_lightgbm_macro_f1')} dan MCC={ctx.get('track_a_lightgbm_mcc')}."
        elif "fitur" in q or "feature" in q or "shap" in q:
            top = bundle.get("top_evidence", [])[:3]
            answer = "Top evidence: " + "; ".join(f"{r.get('feature_group')} ({r.get('hint')})" for r in top)
        elif "batas" in q or "limit" in q:
            answer = bundle.get("claim_boundary", "Jawaban hanya tersedia dari artifact demo.")
        else:
            answer = "Tidak tersedia di artifact demo. Tanya tentang accuracy, Track A, SHAP/fitur, atau batasan klaim."
        return {"answer": answer, "grounding": bundle.get("sources", [])}

    return app


app = create_app()
