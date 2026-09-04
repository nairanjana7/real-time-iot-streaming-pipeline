from pathlib import Path
import sys
import json
import time
import random

from kafka import KafkaProducer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


from backend.core.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
)


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


device_id = random.randint(1000, 9999)


print("\n" + "=" * 70)
print("Random Sensor Producer Started")
print("=" * 70)
print(f"Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"Topic: {KAFKA_TOPIC}")
print(f"Device ID: {device_id}")
print("=" * 70 + "\n")


while True:

    payload = {
        "device_id": device_id,

        # Electrical sensors
        "voltage": round(
            random.uniform(210.0, 240.0),
            2,
        ),

        "current": round(
            random.uniform(5.0, 15.0),
            2,
        ),

        # Machine heat
        "heat": round(
            random.uniform(30.0, 80.0),
            2,
        ),

        # Environmental / machine sensors
        "temperature": round(
            random.uniform(20.0, 50.0),
            2,
        ),

        "humidity": round(
            random.uniform(30.0, 90.0),
            2,
        ),

        "pressure": round(
            random.uniform(950.0, 1050.0),
            2,
        ),

        "vibration": round(
            random.uniform(0.1, 5.0),
            3,
        ),

        "rpm": random.randint(
            1000,
            3000,
        ),

        "timestamp": time.time(),
    }

    try:

        future = producer.send(
            KAFKA_TOPIC,
            payload,
        )

        future.get(timeout=10)

        print("=" * 70)
        print("Telemetry Sent")
        print("=" * 70)
        print(json.dumps(payload, indent=2))
        print("=" * 70)

    except Exception as e:

        print("=" * 70)
        print("Kafka Producer Error")
        print("=" * 70)
        print(e)
        print("=" * 70)

    time.sleep(2)
