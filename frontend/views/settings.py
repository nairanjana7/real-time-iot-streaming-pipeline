import streamlit as st

from services.api_client import api_client


def render_settings():

    st.header("⚙ Settings")

    st.subheader("Application")

    try:

        health = api_client.get_system_health()

        st.write("Project")
        st.code(health["platform"]["name"])

        st.write("Version")
        st.code(health["platform"]["version"])

        st.write("Model")
        st.code(health["model"]["name"])

        st.write("Backend")
        st.success(health["backend"]["status"].capitalize())

        st.write("Streaming Backend")
        st.info(health["streaming"]["backend"])

        st.write("Streaming Status")

        if health["streaming"]["status"] == "connected":
            st.success("Connected")
        elif health["streaming"]["status"] == "unknown":
            st.warning("Unknown")
        else:
            st.error(health["streaming"]["status"].capitalize())

        st.write("License")
        st.code("Open Source")

    except Exception:

        st.error("Unable to connect to the backend.")

        st.info(
            "Start the FastAPI server and refresh the page."
        )
