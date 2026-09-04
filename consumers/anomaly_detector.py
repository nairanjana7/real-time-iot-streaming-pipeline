from kafka import KafkaConsumer
import json
import numpy as np

from backend.core.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
)


WINDOW_SIZE = 30
MIN_SAMPLES = 10
Z_SCORE_THRESHOLD = 2.0


history = {
    "voltage": [],
    "current": [],
    "heat": [],
    "temperature": [],
    "humidity": [],
    "vibration": [],
}


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    ),
)


print(
    "\nZ-Score Anomaly Detector Started..."
)


for message in consumer:

    data = message.value


    print("=" * 70)
    print("Received Telemetry:")
    print(data)


    try:

        values = {
            "voltage": float(
                data["voltage"]
            ),

            "current": float(
                data["current"]
            ),

            "heat": float(
                data["heat"]
            ),

            "temperature": float(
                data["temperature"]
            ),

            "humidity": float(
                data["humidity"]
            ),

            "vibration": float(
                data["vibration"]
            ),
        }


    except (KeyError, TypeError, ValueError) as e:

        print(
            "Skipping telemetry with incompatible schema:",
            e,
        )

        continue


    anomalies = []


    for name, value in values.items():

        history[name].append(value)


        if len(history[name]) > WINDOW_SIZE:

            history[name].pop(0)


        if len(history[name]) < MIN_SAMPLES:

            continue


        mean = np.mean(history[name])

        std = np.std(history[name])


        if std == 0:

            continue


        z_score = (
            value - mean
        ) / std


        print(
            f"{name}: "
            f"value={value:.2f}, "
            f"mean={mean:.2f}, "
            f"z={z_score:.2f}"
        )


        if abs(z_score) > Z_SCORE_THRESHOLD:

            anomalies.append(
                {
                    "feature": name,
                    "value": value,
                    "z_score": round(
                        float(z_score),
                        2,
                    ),
                }
            )


    if anomalies:

        print("\n⚠️ ANOMALY DETECTED")


        for anomaly in anomalies:

            print(
                f"  {anomaly['feature']}: "
                f"value={anomaly['value']}, "
                f"z-score={anomaly['z_score']}"
            )


    else:

        print("\n✓ No anomaly detected")


    print("=" * 70)
