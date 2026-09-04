payload = {
    "machine_id": device_id,

    "voltage": round(
        random.uniform(210, 240),
        2,
    ),

    "current": round(
        random.uniform(5, 20),
        2,
    ),

    "heat": round(
        random.uniform(30, 80),
        2,
    ),

    "temperature": round(
        random.uniform(20, 50),
        2,
    ),

    "pressure": round(
        random.uniform(950, 1050),
        2,
    ),

    "humidity": round(
        random.uniform(30, 90),
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
