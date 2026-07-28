from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = "esp32-data"

device_id = random.randint(1000, 9999)

while True:
    payload = {
        "device_id": device_id,
        "temperature": round(random.uniform(20, 50), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "pressure": round(random.uniform(950, 1050), 2),
        "timestamp": time.time()
    }

    producer.send(TOPIC, payload)
    print("Sent:", payload)

    time.sleep(2)
