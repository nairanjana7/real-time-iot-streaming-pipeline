from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml.preprocessing import preprocess_dataframe
from ml.predictor import FailurePredictor
from ml.explainability import ExplainabilityEngine

from backend.services.report_service import generate_report

# Load model once
predictor = FailurePredictor()
explainer = ExplainabilityEngine(
    predictor.get_model()
)


def predict_machine(machine_data: dict):
    """
    Complete ML Pipeline

    API JSON
        ↓
    Dataset Mapping
        ↓
    Feature Engineering
        ↓
    Random Forest
        ↓
    SHAP
        ↓
    Business Report
    """

    # -------------------------------
    # Convert API schema to AI4I schema
    # -------------------------------

    formatted_data = {
        "Type": machine_data["type"],
        "Air temperature [K]": machine_data["air_temperature"],
        "Process temperature [K]": machine_data["process_temperature"],
        "Rotational speed [rpm]": machine_data["rotational_speed"],
        "Torque [Nm]": machine_data["torque"],
        "Tool wear [min]": machine_data["tool_wear"]
    }

    df = pd.DataFrame([formatted_data])

    processed = preprocess_dataframe(df)

    prediction, probability = predictor.predict(processed)

    print("=" * 50)
    print("Prediction :", prediction)
    print("Probability:", probability)
    print("Type:", type(probability))
    print("=" * 50)

    explanation = explainer.explain(processed)

    report = generate_report(
        probability,
        explanation
    )

    report["prediction"] = (
        "Failure"
        if prediction == 1
        else "Healthy"
    )

    return report
