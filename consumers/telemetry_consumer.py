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
    "TELEMETRY_API_TOKEN"
)


if not BEARER_TOKEN:
    raise RuntimeError(
        "TELEMETRY_API_TOKEN is not configured in .env"
    )


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    ),
)


headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}


print("\nTelemetry Consumer Started...")
print(f"Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"Topic: {KAFKA_TOPIC}")
print(f"Backend: {API_URL}")
print(f"Machine ID: {MACHINE_ID}\n")


for message in consumer:

    data = message.value

    print("=" * 60)
    print("Incoming Kafka Telemetry:")
    print(data)

    try:

        payload = {
            "machine_id": MACHINE_ID,

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

        print("Converted API Payload:")
        print(payload)

        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=10,
        )

        print(
            "API Status:",
            response.status_code,
        )

        print(
            "API Response:",
            response.text,
        )

    except KeyError as e:

        print(
            "Skipping telemetry: missing field",
            e,
        )

    except (TypeError, ValueError) as e:

        print(
            "Skipping telemetry: invalid field value",
            e,
        )

    except requests.RequestException as e:

        print(
            "Telemetry API Error:",
            e,
        )

    print("=" * 60)
