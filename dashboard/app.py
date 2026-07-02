import streamlit as st
import pandas as pd
import json
from kafka import KafkaConsumer

st.set_page_config(page_title="Kafka IoT Dashboard", layout="wide")
st.title("ESP32 Kafka Real-Time Dashboard")

consumer = KafkaConsumer(
    "esp32-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

data = []

placeholder = st.empty()

for msg in consumer:
    payload = msg.value
    data.append(payload)

    df = pd.DataFrame(data)

    latest = df.iloc[-1]

    with placeholder.container():
        col1, col2, col3 = st.columns(3)

        col1.metric("Temperature", f"{latest['temperature']} °C")
        col2.metric("Humidity", f"{latest['humidity']} %")
        col3.metric("Pressure", f"{latest['pressure']} hPa")

        if latest["temperature"] > 45:
            st.error("⚠ High Temperature Detected!")

        if latest["humidity"] < 35:
            st.warning("⚠ Low Humidity Detected!")

        st.subheader("Recent Sensor Data")
        st.dataframe(df.tail(10), use_container_width=True)

        st.subheader("Temperature Trend")
        st.line_chart(df["temperature"])

        st.subheader("Humidity Trend")
        st.line_chart(df["humidity"])

        st.subheader("Pressure Trend")
        st.line_chart(df["pressure"])
