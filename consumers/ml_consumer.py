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


def normalize_telemetry(data):
    """
    Convert AI4I-compatible Kafka telemetry into the format
    expected by the PredictGuard ML service.

    The Random Forest was trained on the AI4I features.
    Therefore voltage/current/heat and other physical sensor
    fields are not passed to the model unless a future model
    is explicitly trained to use them.
    """

    return {
        "type": data["Type"],
        "air_temperature": float(
            data["Air temperature [K]"]
        ),
        "process_temperature": float(
            data["Process temperature [K]"]
        ),
        "rotational_speed": int(
            data["Rotational speed [rpm]"]
        ),
        "torque": float(
            data["Torque [Nm]"]
        ),
        "tool_wear": int(
            data["Tool wear [min]"]
        ),
    }


def run_consumer():

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        value_deserializer=lambda x: json.loads(
            x.decode("utf-8")
        ),
    )

    print("\nML Consumer Started...\n")

    for message in consumer:

        data = message.value

        print("=" * 70)
        print("Incoming Kafka Message")
        print(data)
        print()

        try:

            telemetry = normalize_telemetry(data)

            print("Normalized ML Telemetry")
            print(telemetry)
            print()

            report = predict_machine(
                telemetry
            )

            print("Prediction")
            print(report["prediction"])
            print()

            print("Machine Status")
            print(report["machine_status"])
            print()

            print("Failure Probability")
            print(
                f"{report['failure_probability'] * 100:.2f}%"
            )
            print()

            print("Top Risk Factors")

            for factor in report["top_risk_factors"]:

                print(
                    f"• {factor['feature']} "
                    f"({factor['impact']}) "
                    f"score={factor['score']}"
                )

            print()

            print("Recommendation")
            print(report["recommendation"])

        except KeyError as e:

            print(
                "Skipping message: "
                f"missing ML field {e}"
            )

        except (TypeError, ValueError) as e:

            print(
                "Skipping message: "
                f"invalid ML field value: {e}"
            )

        except Exception as e:

            print(
                "ML Consumer Error:",
                e
            )

        print("=" * 70)


if __name__ == "__main__":
    run_consumer()
