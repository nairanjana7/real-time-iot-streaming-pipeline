import streamlit as st


def render_system_health():

    st.subheader("System Health")

    c1, c2 = st.columns(2)

    with c1:

        st.success("🟢 API")

        st.success("🟢 Kafka")

    with c2:

        st.success("🟢 ML Model")

        st.success("🟢 Backend")
