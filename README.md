# 🔧 Anomalitor – Bearing Health Monitoring

**Predictive Maintenance System for Bearings | NASA IMS Dataset | Random Forest + Docker + Streamlit**

---

## 📌 Project Overview

Anomalitor is an end-to-end predictive maintenance system that detects early bearing failures using vibration data from the NASA IMS dataset.

It combines:
- **Machine Learning** – Random Forest classifier
- **Signal Processing** – FFT for frequency analysis
- **Explainability** – SHAP for model interpretation
- **Production-grade deployment** – FastAPI + PostgreSQL + Docker + Streamlit

---

## 🧠 How It Works
┌─────────────────────────────────────────────────────────────────┐
│ Vibration Data (NASA IMS Bearing Dataset) │
│ → Feature Extraction (RMS, FFT) │
│ → Random Forest Model (Residual-based anomaly detection) │
│ → FastAPI (Serving predictions) │
│ → PostgreSQL (Storing history) │
│ → Streamlit Dashboard (Visualizing results) │
└─────────────────────────────────────────────────────────────────┘

### Detection Logic

1. **Feature Engineering:** Extract RMS (Root Mean Square) from raw vibration signals.
2. **Model Training:** Train Random Forest Regressor on **healthy** bearings only.
3. **Prediction:** Model predicts expected `ratio = rms_b3 / rms_b1`.
4. **Residual Calculation:** `residual = |actual_ratio - predicted_ratio|`.
5. **Anomaly Decision:** If `residual > threshold` → **Anomaly detected**.

### Threshold Selection

- The threshold was calibrated on the NASA IMS dataset.
- Domain-specific feature: `ratio = RMS_B3 / RMS_B1` compares the suspicious bearing to a healthy reference.

---

## 📊 Results

### 1. Model Performance (Comparison)

| Model      | Accuracy |
|------------|----------|
| **Random Forest** | 99.54% |
| LightGBM   | 99.31% |
| MLP        | 99.31% |
| XGBoost    | 99.07% |

### 2. Anomaly Detection

- The system detects anomalies when the residual exceeds the calibrated threshold.
- Validated on historical NASA bearing records.

### 3. Failure Identification (FFT + BPFI)

- **Bearing 3** identified with inner race defect.
- **BPFI ≈ 300 Hz** (calculated: `0.6 × 33.33 Hz × 15 balls`).
- **FFT shows a clear peak at ~300 Hz** in the failed bearing.

### 4. Model Explainability (SHAP)

- `rms_b3` contributes significantly to the model's decision.
- SHAP analysis confirms the model's focus on the correct bearing.

### 5. Stability (Monte Carlo)

- The model maintains stable performance under noise (2% injected noise, 1000 iterations).
- Methodology documented for reproducibility.

---

## 🛠️ Tech Stack

| Component       | Technology                     |
|-----------------|--------------------------------|
| **ML Framework** | Scikit-learn (Random Forest)   |
| **Signal Processing** | FFT (SciPy), SHAP            |
| **API**         | FastAPI, Uvicorn               |
| **Database**    | PostgreSQL (via SQLAlchemy)    |
| **Dashboard**   | Streamlit + Plotly             |
| **Containerization** | Docker, Docker Compose    |
| **Language**    | Python 3.10                    |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (for local development)

### Run with Docker

```bash
git clone https://github.com/eliyahudahan/anomalitor.git
cd anomalitor
docker compose up --build
Then open:

API: http://localhost:8000

Dashboard: http://localhost:8501

Test the API
bash
# Health check
curl http://localhost:8000/health

# Predict anomaly
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"rms_b1": 0.125, "rms_b3": 0.500}'
📂 Project Structure
'''text
anomalitor/
├── app/
│   └── main.py                # FastAPI endpoints
├── src/
│   ├── database/
│   │   ├── config.py          # DB connection (SQLAlchemy)
│   │   └── models.py          # Table schema (BearingRecord)
│   └── models/
│       └── rf_residual.py     # Random Forest model
├── scripts/
│   ├── empirical_validation.py
│   ├── monte_carlo.py
│   ├── fft_analysis.py
│   └── shap_analysis.py
├── data/
│   └── nasa/
│       └── processed/
│           └── set1_features.csv
├── notebooks/
│   ├── 01_eda_nasa.ipynb
│   ├── 02_model_comparison.ipynb
│   └── 03_anomaly_detection.ipynb
├── dashboard.py               # Streamlit dashboard
├── entrypoint.sh              # Docker container entrypoint
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
📈 Dashboard Preview
The Streamlit dashboard includes:

- 📊 Real-time ratio chart (B3/B1) with anomaly markers
- 📋 Recent anomalies table
- 🧠 SHAP feature importance (model explainability)
- 🔬 FFT spectrum (healthy vs failed bearing)
- 📍 BPFI calculation (inner race fault identification)

🤝 Acknowledgments
NASA IMS Bearing Dataset – IMS Center, University of Cincinnati

Rexnord ZA-2115 bearing specifications

Open-source libraries: Scikit-learn, FastAPI, Streamlit, SQLAlchemy, Docker

📝 Author
Eliyahu Dahan
📧 framgangsrik747@gmail.com
🔗 LinkedIn
🐙 GitHub

📅 Project Timeline
Phase	Completed
EDA + Feature Engineering	✅ 24.05
Model Comparison	✅ 26.05
Anomaly Detection	✅ 28.05
PostgreSQL + FastAPI	✅ 31.05
Docker + Streamlit	✅ 03.06
BONUS: Lead Time, SHAP, FFT, Monte Carlo	✅ 13.06
Empirical Validation	✅ 14.06
Project Complete	✅ 17.06.2026
🎯 Conclusion
Anomalitor is a complete, explainable, and validated predictive maintenance system.
It demonstrates end-to-end capability – from raw vibration data to a live dashboard – on the NASA IMS bearing dataset.

Ready to run. 🚀