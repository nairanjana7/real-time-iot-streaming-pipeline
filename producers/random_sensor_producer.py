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

print("\nRandom Sensor Producer Started...\n")

while True:

    payload = {
        "device_id": device_id,

        "temperature": round(
            random.uniform(20, 50),
            2,
        ),

        "humidity": round(
            random.uniform(30, 90),
            2,
        ),

        "pressure": round(
            random.uniform(950, 1050),
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

    producer.send(
        KAFKA_TOPIC,
        payload,
    )

    producer.flush()

    print("Sent:", payload)

    time.sleep(2)
