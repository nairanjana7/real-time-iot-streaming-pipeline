from pathlib import Path
import sys
import json

from kafka import KafkaConsumer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.ml_service import predict_machine


consumer = KafkaConsumer(
    "esp32-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("\nML Consumer Started...\n")

for message in consumer:

    data = message.value

    try:

        report = predict_machine(data)

        print("=" * 70)

        print("Incoming Telemetry")

        print(data)

        print()

        print("Prediction")

        print(report["prediction"])

        print()

        print("Machine Status")

        print(report["machine_status"])

        print()

        print("Failure Probability")

        print(f"{report['failure_probability']}%")

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
