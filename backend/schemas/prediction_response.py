from pydantic import BaseModel
from typing import List


class RiskFactor(BaseModel):
    feature: str
    impact: str
    score: float


class PredictionResult(BaseModel):
    machine_status: str
    failure_detected: bool
    failure_probability: float


class ExplanationResult(BaseModel):
    recommendation: str
    top_risk_factors: List[RiskFactor]


class MetadataResult(BaseModel):
    model_name: str
    model_version: str
    prediction_timestamp: str

class PredictionResponse(BaseModel):
    prediction: PredictionResult
    explanation: ExplanationResult
    metadata: MetadataResult
