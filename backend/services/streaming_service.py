import socket

from backend.config import STREAMING_BACKEND
from backend.core.kafka_config import KAFKA_BOOTSTRAP_SERVERS


def get_streaming_status():

    backend = STREAMING_BACKEND

    if backend.lower() == "kafka":

        host, port = KAFKA_BOOTSTRAP_SERVERS.rsplit(":", 1)
        port = int(port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((host, port))
            status = "connected"

        except Exception:
            status = "disconnected"

        finally:
            sock.close()

        return {
            "backend": backend,
            "status": status,
        }

    return {
        "backend": backend,
        "status": "unknown",
    }
