kimport streamlit as st


def render_kpi_strip(prediction):

    probability = prediction["prediction"]["failure_probability"]

    if probability >= 70:
        healthy = 0
        warning = 0
        high_risk = 1

    elif probability >= 30:
        healthy = 0
        warning = 1
        high_risk = 0

    else:
        healthy = 1
        warning = 0
        high_risk = 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Machines",
            1
        )

    with c2:
        st.metric(
            "Healthy",
            healthy
        )

    with c3:
        st.metric(
            "Warning",
            warning
        )

    with c4:
        st.metric(
            "High Risk",
            high_risk
        )
