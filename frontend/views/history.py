import streamlit as st


def render_history():

    st.header("📜 Prediction History")

    st.caption(

        "Historical prediction records"

    )

    st.warning(

        "No prediction history available."

    )

    st.info(

        "Prediction history will automatically appear after PostgreSQL integration."

    )
