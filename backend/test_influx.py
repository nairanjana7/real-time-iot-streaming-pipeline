from backend.database.influx import client

try:
    health = client.health()

    print("\nInfluxDB Connected Successfully!")
    print(f"Status : {health.status}")
    print(f"Version: {health.version}")

except Exception as e:
    print(e)
