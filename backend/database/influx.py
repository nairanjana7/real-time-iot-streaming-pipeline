import os
from pathlib import Path

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, WriteOptions

from backend.core.config import settings


load_dotenv(
    Path(__file__).resolve().parents[2] / ".env"
)


print("URL:", settings.INFLUX_URL)
print("ORG:", settings.INFLUX_ORG)
print("TOKEN FOUND:", bool(settings.INFLUX_TOKEN))


client = InfluxDBClient(
    url=settings.INFLUX_URL,
    token=settings.INFLUX_TOKEN,
    org=settings.INFLUX_ORG,
)


write_api = client.write_api(
    write_options=WriteOptions(
        batch_size=1,
        flush_interval=1_000,
        jitter_interval=0,
        retry_interval=5_000,
    )
)

query_api = client.query_api()
