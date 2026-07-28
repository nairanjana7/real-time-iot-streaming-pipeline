from kafka import KafkaProducer
import pandas as pd
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = "esp32-data"

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
            "Tool wear [min]": int(row["Tool wear [min]"])
        }

        producer.send(TOPIC, payload)

        print(payload)

        time.sleep(1)
