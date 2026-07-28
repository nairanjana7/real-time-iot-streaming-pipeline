import streamlit as st


def render_sidebar():

    st.sidebar.markdown("# 🏭")

    st.sidebar.title("PredictGuard AI")

    st.sidebar.markdown("---")

    page = st.sidebar.radio(

        "Navigation",

        [

            "Dashboard",

            "Analytics",

            "History",

            "Settings"

        ]

    )

    st.sidebar.markdown("---")

    st.sidebar.caption("Open Source Platform")

    st.sidebar.caption("Version 1.0.0")

    return page
