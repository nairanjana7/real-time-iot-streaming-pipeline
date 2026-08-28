from kafka import KafkaProducer
import pandas as pd
import json
import time

from backend.core.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

df = pd.read_csv(
    "data/ai4i+2020+predictive+maintenance+dataset/ai4i2020.csv"
)

print("Streaming AI4I Dataset...\n")

while True:

    for _, row in df.iterrows():

        payload = {
            "Type": row["Type"],
            "Air temperature [K]": float(row["Air temperature [K]"]),
            "Process temperature [K]": float(row["Process temperature [K]"]),
            "Rotational speed [rpm]": int(row["Rotational speed [rpm]"]),
            "Torque [Nm]": float(row["Torque [Nm]"]),
            "Tool wear [min]": int(row["Tool wear [min]"]),
        }

        producer.send(KAFKA_TOPIC, payload)

        print(payload)

        time.sleep(1)
