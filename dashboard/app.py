import streamlit as st
import pandas as pd
import json
from kafka import KafkaConsumer

st.set_page_config(
    page_title="Kafka IoT Dashboard",
    layout="wide"
)

st.title("ESP32 Kafka Real-Time Dashboard")

consumer = KafkaConsumer(
    "esp32-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)

data = []

placeholder = st.empty()

for msg in consumer:

    payload = msg.value
    data.append(payload)

    df = pd.DataFrame(data)
    latest = df.iloc[-1]

    with placeholder.container():

        # -------------------------------------------------
        # Existing + New Sensor Metrics
        # -------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Temperature",
            f"{latest['temperature']} °C"
        )

        col2.metric(
            "Humidity",
            f"{latest['humidity']} %"
        )

        col3.metric(
            "Pressure",
            f"{latest['pressure']} hPa"
        )

        col4.metric(
            "RPM",
            f"{latest['rpm']}"
        )

        col5, col6, col7 = st.columns(3)

        col5.metric(
            "Voltage",
            f"{latest['voltage']} V"
        )

        col6.metric(
            "Current",
            f"{latest['current']} A"
        )

        col7.metric(
            "Heat",
            f"{latest['heat']} °C"
        )

        # -------------------------------------------------
        # Simple Sensor Warnings
        # -------------------------------------------------

        if latest["temperature"] > 45:
            st.error(
                "⚠ High Temperature Detected!"
            )

        if latest["humidity"] < 35:
            st.warning(
                "⚠ Low Humidity Detected!"
            )

        if latest["heat"] > 75:
            st.warning(
                "⚠ High Machine Heat Detected!"
            )

        if latest["voltage"] < 210 or latest["voltage"] > 240:
            st.warning(
                "⚠ Voltage Outside Normal Range!"
            )

        if latest["current"] < 5 or latest["current"] > 15:
            st.warning(
                "⚠ Current Outside Normal Range!"
            )

        # -------------------------------------------------
        # Recent Sensor Data
        # -------------------------------------------------

        st.subheader("Recent Sensor Data")

        st.dataframe(
            df.tail(10),
            use_container_width=True
        )

        # -------------------------------------------------
        # Trends
        # -------------------------------------------------

        st.subheader("Temperature Trend")
        st.line_chart(df["temperature"])

        st.subheader("Humidity Trend")
        st.line_chart(df["humidity"])

        st.subheader("Pressure Trend")
        st.line_chart(df["pressure"])

        st.subheader("Voltage Trend")
        st.line_chart(df["voltage"])

        st.subheader("Current Trend")
        st.line_chart(df["current"])

        st.subheader("Machine Heat Trend")
        st.line_chart(df["heat"])
