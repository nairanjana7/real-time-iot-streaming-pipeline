from typing import Dict
import numpy as np


def machine_status(probability: float) -> str:

    if probability >= 0.80:
        return "🔴 Critical"

    elif probability >= 0.50:
        return "🟠 High Risk"

    elif probability >= 0.20:
        return "🟡 Warning"

    return "🟢 Healthy"


def recommendation(status: str) -> str:

    recommendations = {

        "🔴 Critical":
            "Immediate inspection required. Stop machine if necessary.",

        "🟠 High Risk":
            "Schedule maintenance within the next maintenance window.",

        "🟡 Warning":
            "Monitor machine closely and inspect during routine maintenance.",

        "🟢 Healthy":
            "Continue normal operation."

    }

    return recommendations[status]


def top_risk_factors(explanation, top_n: int = 3):

    values = explanation.values[0]

    feature_names = explanation.feature_names

    # Class-1 (Failure) SHAP values
    contributions = values[:, 1]

    indices = np.argsort(
        np.abs(contributions)
    )[::-1][:top_n]

    factors = []

    for idx in indices:

        factors.append({

            "feature": feature_names[idx],

            "impact":
                "Increasing Risk"
                if contributions[idx] > 0
                else "Reducing Risk",

            "score":
                round(float(contributions[idx]), 4)

        })

    return factors


def generate_report(
    probability: float,
    explanation
) -> Dict:

    status = machine_status(probability)

    report = {

        "machine_status": status,

        "failure_probability":
            round(probability, 4),

        "recommendation":
            recommendation(status),

        "top_risk_factors":
            top_risk_factors(explanation)

    }

    return report
