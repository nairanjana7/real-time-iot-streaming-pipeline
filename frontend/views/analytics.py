import streamlit as st
import plotly.graph_objects as go


def render_analytics():

    st.header("📊 Analytics")

    st.caption(
        "Fleet Risk Analytics"
    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=["Mon","Tue","Wed","Thu","Fri"],

            y=[4,7,6,8,5],

            mode="lines+markers",

            line=dict(width=3)

        )

    )

    fig.update_layout(

        title="Average Fleet Risk",

        height=400

    )

    st.plotly_chart(

        fig,

        width="stretch"

    )

    st.info(

        "Historical analytics will be powered by PostgreSQL."

    )
