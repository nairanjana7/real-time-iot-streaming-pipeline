from kafka import KafkaConsumer
import json
import numpy as np

from backend.core.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
)


temps = []
humidity_values = []

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print("Z-Score Anomaly Detector Started...")


for message in consumer:

    data = message.value

    try:
        temp = data["temperature"]
        humidity = data["humidity"]
    except KeyError:
        print("Skipping telemetry with incompatible schema:", data)
        continue

    temps.append(temp)
    humidity_values.append(humidity)

    if len(temps) > 30:
        temps.pop(0)
        humidity_values.pop(0)

    print("Received:", data)

    if len(temps) >= 10:

        mean_temp = np.mean(temps)
        std_temp = np.std(temps)

        if std_temp != 0:

            z_score = (temp - mean_temp) / std_temp

            print(f"Z-score: {z_score:.2f}")

            if abs(z_score) > 2:

                print("ANOMALY DETECTED!")

                print(
                    f"Temperature={temp}, "
                    f"Mean={mean_temp:.2f}, "
                    f"Std={std_temp:.2f}"
                )
