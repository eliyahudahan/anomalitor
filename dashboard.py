import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import os
from PIL import Image

st.set_page_config(page_title="Anomalitor Dashboard", layout="wide")
st.title("🔧 Anomalitor – Bearing Health Monitoring")

# התחבר ל-DB
conn = psycopg2.connect(
    host="db",
    database="anomalitor_db",
    user="framg",
    password=os.getenv("DB_PASSWORD", "your_password")
)

# קריאת נתונים
df = pd.read_sql("SELECT * FROM bearing_records ORDER BY id", conn)
conn.close()

# ================================
# כרטיסי ביצועים
# ================================
st.subheader("📊 Model Performance")
col1, col2 = st.columns(2)
col1.metric("Total Predictions", len(df))
col2.metric("Anomalies Detected", len(df[df['detected_anomaly'] == 1]) if len(df) > 0 else 0)

# ================================
# גרף Ratio לאורך זמן
# ================================
if len(df) > 0:
    st.subheader("📈 Ratio (B3/B1) Over Time")
    fig = px.line(df, x='timestamp', y='ratio', color='detected_anomaly',
                  title="Bearing Degradation Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ================================
# טבלת אנומליות אחרונות
# ================================
if len(df) > 0:
    st.subheader("⚠️ Recent Anomalies")
    anomalies = df[df['detected_anomaly'] == 1][['timestamp', 'rms_b1', 'rms_b3', 'ratio', 'residual']]
    st.dataframe(anomalies)

# ================================
# Precision-Recall Curve (Lead Time)
# ================================
st.subheader("⚖️ Threshold Optimization (Precision-Recall)")
st.image("precision_recall_curve.png", caption="Precision-Recall Trade-off", use_container_width=False)

# ================================
# SHAP Feature Importance
# ================================
st.subheader("🧠 Model Explainability (SHAP)")
st.image("shap_summary.png", caption="Feature Impact on Prediction", use_container_width=False)

# ================================
# FFT Analysis – Healthy vs Failed
# ================================
st.subheader("🔬 Frequency Domain Analysis (FFT)")
col3, col4 = st.columns(2)
with col3:
    st.image("fft_healthy.png", caption="Healthy Bearing (Start of Test)")
with col4:
    st.image("fft_failed.png", caption="Failed Bearing (End of Test)")

# ================================
# Monte Carlo Stability
# ================================
st.subheader("🎲 Monte Carlo Simulation (Stability Test)")
st.image("monte_carlo_boxplots.png", caption="Precision & Recall Distribution (1000 iterations)", use_container_width=False)

# ================================
# Threshold Tradeoff (FP vs FN)
# ================================
st.subheader("📊 False Positives vs False Negatives by Threshold")
st.image("threshold_tradeoff_full.png", caption="FP/FN vs Threshold (Full Dataset)", use_container_width=False)

# ================================
# הסבר על הסף הנבחר
# ================================
st.subheader("✅ Selected Threshold: 1.2")
st.markdown("""
- **Why 1.2?** The lowest threshold that perfectly separates normal (ratio ≈ 1.0) from failure (ratio ≥ 4.0)
- **Results on 2,156 historical records:**  
  - False Positives: **0**  
  - False Negatives: **0**  
  - Precision: **1.00**, Recall: **1.00**, F1: **1.00**
- **Business decision:** In predictive maintenance, early warning is critical. No cost to false alarms.
""")