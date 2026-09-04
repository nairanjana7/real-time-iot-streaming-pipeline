import numpy as np

from backend.services.report_service import (
    machine_status,
    recommendation,
    top_risk_factors,
    generate_report,
)


class FakeExplanation:
    def __init__(self):
        self.values = np.array([[
            [0.0, 0.10],
            [0.0, -0.40],
            [0.0, 0.20],
            [0.0, -0.05],
        ]])

        self.feature_names = [
            "temperature",
            "pressure",
            "vibration",
            "rpm",
        ]


def test_machine_status_thresholds():
    assert machine_status(0.80) == "🔴 Critical"
    assert machine_status(0.50) == "🟠 High Risk"
    assert machine_status(0.20) == "🟡 Warning"
    assert machine_status(0.19) == "🟢 Healthy"


def test_machine_status_extreme_values():
    assert machine_status(0.0) == "🟢 Healthy"
    assert machine_status(1.0) == "🔴 Critical"


def test_recommendations_match_status():
    assert "Immediate inspection" in recommendation("🔴 Critical")
    assert "Schedule maintenance" in recommendation("🟠 High Risk")
    assert "Monitor machine" in recommendation("🟡 Warning")
    assert "normal operation" in recommendation("🟢 Healthy")


def test_top_risk_factors_order_and_direction():
    explanation = FakeExplanation()

    factors = top_risk_factors(explanation, top_n=3)

    assert [f["feature"] for f in factors] == [
        "pressure",
        "vibration",
        "temperature",
    ]

    assert factors[0]["impact"] == "Reducing Risk"
    assert factors[0]["score"] == -0.40

    assert factors[1]["impact"] == "Increasing Risk"
    assert factors[1]["score"] == 0.20


def test_top_risk_factors_handles_reducing_risk():
    explanation = FakeExplanation()

    factors = top_risk_factors(explanation, top_n=4)

    assert factors[1]["impact"] == "Increasing Risk"
    assert factors[3]["impact"] == "Reducing Risk"


def test_generate_report_structure():
    explanation = FakeExplanation()

    report = generate_report(
        probability=0.65,
        explanation=explanation,
    )

    assert report["machine_status"] == "🟠 High Risk"
    assert report["failure_probability"] == 0.65
    assert "recommendation" in report
    assert "top_risk_factors" in report
    assert len(report["top_risk_factors"]) == 3
