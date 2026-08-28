from pathlib import Path
import sys
import json

from kafka import KafkaConsumer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
)

from backend.services.ml_service import predict_machine


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print("\nML Consumer Started...\n")


def normalize_telemetry(data):
    """
    Convert AI4I Kafka telemetry format into the format
    expected by the PredictGuard ML service.
    """

    return {
        "type": data["Type"],
        "air_temperature": data["Air temperature [K]"],
        "process_temperature": data["Process temperature [K]"],
        "rotational_speed": data["Rotational speed [rpm]"],
        "torque": data["Torque [Nm]"],
        "tool_wear": data["Tool wear [min]"],
    }


for message in consumer:

    data = message.value

    try:

        telemetry = normalize_telemetry(data)

        report = predict_machine(telemetry)

        print("=" * 70)

        print("Incoming Telemetry")
        print(data)

        print()

        print("Normalized Telemetry")
        print(telemetry)

        print()

        print("Prediction")
        print(report["prediction"])

        print()

        print("Machine Status")
        print(report["machine_status"])

        print()

        print("Failure Probability")
        print(f"{report['failure_probability'] * 100:.2f}%")

        print()

        print("Top Risk Factors")

        for factor in report["top_risk_factors"]:
            print(
                f"• {factor['feature']} "
                f"({factor['impact']})"
            )

        print()

        print("Recommendation")
        print(report["recommendation"])

        print("=" * 70)

    except Exception as e:

        print("Consumer Error:", e)
