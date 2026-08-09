markdown
# 🔧 Anomalitor – Bearing Health Monitoring

**Predictive Maintenance System for Bearings | NASA IMS Dataset | Random Forest + Docker + Streamlit**

---

## 📌 Project Overview

Anomalitor is an end-to-end predictive maintenance system that detects early bearing failures using vibration data from the NASA IMS dataset.

It combines:
- **Machine Learning** – Random Forest classifier
- **Signal Processing** – FFT for frequency analysis
- **Explainability** – SHAP for model interpretation
- **Deployment** – FastAPI + PostgreSQL + Docker + Streamlit

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

text

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
- Docker & Docker Compose (for containerized run)
- Python 3.10+ (for local development)

---

### Run with Docker (Recommended)

```bash
git clone https://github.com/eliyahudahan/anomalitor.git
cd anomalitor
docker compose up --build
What this starts:

PostgreSQL (db) – stores bearing records

FastAPI (api) – serves predictions on port 8000

Streamlit (streamlit) – interactive dashboard on port 8501

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
Run without Docker (Local Development)
Why: For development, debugging, or when Docker is not available.

Note: The db hostname only works inside Docker. For local development, you must change it to localhost.

Step 1: Install dependencies

bash
pip install -r requirements.txt
Step 2: Set up PostgreSQL locally

bash
# Install PostgreSQL (if not already installed)
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql

# Create database
createdb anomalitor
Step 3: Update dashboard.py
Open dashboard.py and change line 12:

python
# Before:
host="db"

# After:
host="localhost"
Step 4: Run the dashboard

bash
streamlit run dashboard.py
📂 Project Structure
text
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
The Streamlit dashboard provides an interactive view of the NASA IMS dataset:

📊 Ratio chart (B3/B1) with anomaly markers

📋 Recent anomalies table

🧠 SHAP feature importance

🔬 FFT spectrum (healthy vs failed bearing)

📍 BPFI calculation (inner race fault identification)

Note: This dashboard reads from a PostgreSQL database populated with historical NASA IMS data. It is interactive (you can filter, explore, and analyze) but not live – no real-time sensor data is being ingested.

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
It demonstrates end-to-end capability – from raw vibration data to an interactive dashboard – on the NASA IMS bearing dataset.

What this project shows:

Full pipeline: Data ingestion → Feature engineering → Model training → API → Database → Dashboard

Model robustness: Monte Carlo test (1000 iterations, 2% noise) – stable performance

Explainability: SHAP analysis + FFT spectrum + BPFI calculation – you can see why the model makes decisions

Note: The model achieves perfect separation on the NASA IMS dataset, but this is not a claim of real-world performance. This is a controlled lab experiment that demonstrates my ability to build a complete pipeline from raw data to visualization.

Ready to run. 🚀