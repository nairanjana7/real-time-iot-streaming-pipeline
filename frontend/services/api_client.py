import requests

from utils.constants import (
    API_BASE_URL,
    PREDICTION_ENDPOINT,
    SYSTEM_HEALTH_ENDPOINT,
)


class APIClient:

    def __init__(self):

        self.base_url = API_BASE_URL

    def predict(self, telemetry):

        response = requests.post(

            self.base_url + PREDICTION_ENDPOINT,

            json=telemetry,

            timeout=10

        )

        response.raise_for_status()

        return response.json()

    def get_system_health(self):

        response = requests.get(

            self.base_url + SYSTEM_HEALTH_ENDPOINT,

            timeout=5

        )

        response.raise_for_status()

        return response.json()


api_client = APIClient()
