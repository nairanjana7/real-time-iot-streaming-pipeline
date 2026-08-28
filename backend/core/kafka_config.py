import os

from dotenv import load_dotenv

from backend.core.config import BASE_DIR

load_dotenv(BASE_DIR / ".env")


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "esp32-data",
)

BACKEND_API_URL = os.getenv(
    "BACKEND_API_URL",
    "http://localhost:8000",
)
