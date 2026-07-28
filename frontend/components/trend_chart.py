import plotly.graph_objects as go

import streamlit as st


def render_trend_chart():

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=[1,2,3,4,5,6],

            y=[5,9,15,18,22,21],

            mode="lines+markers",

            name="Risk"

        )

    )

    fig.update_layout(

        title="Risk Trend",

        height=350,

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )

    )

    st.plotly_chart(
    fig,
    width="stretch"
)
