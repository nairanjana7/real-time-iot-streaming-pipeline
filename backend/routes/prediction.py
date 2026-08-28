from datetime import datetime, timezone

from fastapi import APIRouter

from ml.config import MODEL_NAME, MODEL_VERSION

from backend.schemas.telemetry_request import TelemetryRequest

from backend.schemas.prediction_response import (
    PredictionResponse,
    PredictionResult,
    ExplanationResult,
    MetadataResult,
    RiskFactor,
)

from backend.services.ml_service import predict_machine

router = APIRouter(
    prefix="/api/v1/prediction",
    tags=["Prediction"]
)


@router.post(
    "/",
    response_model=PredictionResponse
)
def predict(request: TelemetryRequest):

    report = predict_machine(
        request.model_dump()
    )

    prediction = PredictionResult(
        machine_status=report["machine_status"],
        failure_detected=report["prediction"] == "Failure",
        failure_probability=report["failure_probability"],
    )

    explanation = ExplanationResult(
        recommendation=report["recommendation"],
        top_risk_factors=[
            RiskFactor(**factor)
            for factor in report["top_risk_factors"]
        ],
    )

    metadata = MetadataResult(
    model_name=MODEL_NAME,
    model_version=MODEL_VERSION,
    prediction_timestamp=datetime.now(timezone.utc).isoformat()
)

    return PredictionResponse(
        prediction=prediction,
        explanation=explanation,
        metadata=metadata,
    )
