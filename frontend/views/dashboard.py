import streamlit as st

from services.dashboard_service import get_dashboard_data

from components.kpi_strip import render_kpi_strip
from components.machine_card import render_machine_card
from components.system_health import render_system_health
from components.trend_chart import render_trend_chart


def render_dashboard():

    try:

        dashboard_data = get_dashboard_data()

    except Exception as e:

        st.error("Unable to load dashboard data.")

        with st.expander("Technical Details"):
            st.code(str(e))

        return

    prediction = dashboard_data["prediction"]
    health = dashboard_data["health"]

    render_kpi_strip(prediction)

    st.write("")

    machine = {

        "machine_name": "Machine L-213",

        "machine_type": "Type L",

        "failure_probability": prediction["prediction"]["failure_probability"],

        "torque": 43.7,

        "tool_wear": 217,

        "rpm": 1355,

        "risk_factors": [

            factor["feature"]

            for factor in prediction["explanation"]["top_risk_factors"]

        ]

    }

    render_machine_card(machine)

    st.write("")

    render_trend_chart()

    st.write("")

    render_system_health(health)
