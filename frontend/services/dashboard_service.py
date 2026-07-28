import streamlit as st

from services.api_client import api_client


@st.cache_data(ttl=5)
def get_dashboard_data():

    """
    Temporary dashboard data.

    Later this function will aggregate:
    - Prediction API
    - History
    - Analytics
    - Health
    """

    telemetry = {

        "type": "L",

        "air_temperature": 298.5,

        "process_temperature": 308.2,

        "rotational_speed": 1355,

        "torque": 43.7,

        "tool_wear": 217

    }

    prediction = api_client.predict(telemetry)

    health = api_client.get_system_health()

    return {

        "prediction": prediction,

        "health": health

    }
