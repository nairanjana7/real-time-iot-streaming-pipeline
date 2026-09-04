from pathlib import Path
import sys
import json
import os
import requests

from dotenv import load_dotenv
from kafka import KafkaConsumer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


from backend.core.config import BASE_DIR

from backend.core.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    BACKEND_API_URL,
)


load_dotenv(BASE_DIR / ".env")


API_URL = f"{BACKEND_API_URL}/api/v1/telemetry/"


MACHINE_ID = int(
    os.getenv(
        "TELEMETRY_MACHINE_ID",
        "1",
    )
)


BEARER_TOKEN = os.getenv(
    "TELEMETRY_DEVICE_API_KEY"
)


if not BEARER_TOKEN:
    raise RuntimeError(
        "TELEMETRY_DEVICE_API_KEY is not configured in .env"
    )


def create_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        value_deserializer=lambda x: json.loads(
            x.decode("utf-8")
        ),
    )


def build_payload(data):
    """
    Convert Kafka telemetry into the backend telemetry schema.

    The ML-related machine variables remain separate from
    the new monitoring-only sensors.
    """

    return {
        "machine_id": MACHINE_ID,

        # New monitoring sensors
        "voltage": float(
            data["voltage"]
        ),

        "current": float(
            data["current"]
        ),

        "heat": float(
            data["heat"]
        ),

        # Existing telemetry
        "temperature": float(
            data["temperature"]
        ),

        "pressure": float(
            data["pressure"]
        ),

        "humidity": float(
            data["humidity"]
        ),

        "vibration": float(
            data["vibration"]
        ),

        "rpm": int(
            data["rpm"]
        ),
    }


def run_consumer():

    consumer = create_consumer()

    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json",
    }

    print("\n" + "=" * 70)
    print("Telemetry Consumer Started")
    print("=" * 70)
    print(f"Kafka:   {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"Topic:   {KAFKA_TOPIC}")
    print(f"Backend: {API_URL}")
    print(f"Machine: {MACHINE_ID}")
    print("=" * 70 + "\n")

    for message in consumer:

        data = message.value

        print("=" * 70)
        print("Incoming Kafka Telemetry")
        print(json.dumps(data, indent=2))

        try:

            payload = build_payload(data)

            print("\nConverted Backend Payload")
            print(json.dumps(payload, indent=2))

            response = requests.post(
                API_URL,
                json=payload,
                headers=headers,
                timeout=10,
            )

            print("\nAPI Status:", response.status_code)
            print("API Response:", response.text)

            if response.ok:
                print("\n✓ Telemetry successfully stored")
            else:
                print("\n✗ Backend rejected telemetry")

        except KeyError as e:

            print(
                "\nSkipping telemetry: "
                f"missing field {e}"
            )

        except (TypeError, ValueError) as e:

            print(
                "\nSkipping telemetry: "
                f"invalid field value: {e}"
            )

        except requests.RequestException as e:

            print(
                "\nTelemetry API Error:",
                e,
            )

        print("=" * 70)


if __name__ == "__main__":
    run_consumer()
