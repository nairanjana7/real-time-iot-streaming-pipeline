from kafka import KafkaConsumer
import json
import numpy as np

temps = []
humidity_values = []

consumer = KafkaConsumer(
    "esp32-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Z-Score Anomaly Detector Started...")

for message in consumer:
    data = message.value
    temp = data["temperature"]
    humidity = data["humidity"]

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
                    f"Temperature={temp}, Mean={mean_temp:.2f}, Std={std_temp:.2f}"
                )
