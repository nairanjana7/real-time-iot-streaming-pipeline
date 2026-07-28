from datetime import datetime, timezone

from backend.config import (
    PLATFORM_NAME,
    PLATFORM_VERSION,
    MODEL_NAME,
    MODEL_VERSION,
)

from backend.services.streaming_service import get_streaming_status


def get_system_health():

    return {

        "backend": {
            "status": "connected"
        },

        "streaming": get_streaming_status(),

        "model": {
            "status": "loaded",
            "name": MODEL_NAME,
            "version": MODEL_VERSION
        },

        "platform": {
            "name": PLATFORM_NAME,
            "version": PLATFORM_VERSION
        },

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()

    }
