import streamlit as st


def render_header():

    col1, col2 = st.columns([6, 1])

    with col1:

        st.title("🏭 PredictGuard AI")

        st.caption(
            "Industrial Predictive Maintenance Platform"
        )

    with col2:

        st.success("API")

    st.divider()
