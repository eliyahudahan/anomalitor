import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Anomalitor Dashboard", layout="wide")
st.title("🔧 Anomalitor – Bearing Health Monitoring")

# חיבור ל-DB (בתוך רשת Docker)
conn = psycopg2.connect(
    host="db",
    database="anomalitor_db",
    user="framg",
    password=os.getenv("DB_PASSWORD", "your_password")
)

df = pd.read_sql("SELECT * FROM bearing_records ORDER BY id", conn)

st.subheader("📈 Ratio (B3/B1) Over Time")
fig = px.line(df, x='timestamp', y='ratio', color='detected_anomaly', 
              title="Bearing Degradation Trend", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("⚠️ Recent Anomalies")
anomalies = df[df['detected_anomaly'] == 1][['timestamp', 'rms_b1', 'rms_b3', 'ratio', 'residual']]
st.dataframe(anomalies)

st.subheader("📊 Model Performance")
col1, col2 = st.columns(2)
col1.metric("Total Predictions", len(df))
col2.metric("Anomalies Detected", len(anomalies))
