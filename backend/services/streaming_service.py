import socket

from backend.config import STREAMING_BACKEND


KAFKA_HOST = "localhost"
KAFKA_PORT = 9092


def get_streaming_status():

    backend = STREAMING_BACKEND

    if backend.lower() == "kafka":

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((KAFKA_HOST, KAFKA_PORT))
            status = "connected"

        except Exception:
            status = "disconnected"

        finally:
            sock.close()

        return {
            "backend": backend,
            "status": status
        }

    return {
        "backend": backend,
        "status": "unknown"
    }
