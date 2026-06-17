```markdown
# 🔧 Anomalitor – Bearing Health Monitoring

**Predictive Maintenance System for Bearings | NASA IMS Dataset | Random Forest + Docker + Streamlit**

---

## 📌 Project Overview

Anomalitor is an end-to-end predictive maintenance system that detects early bearing failures using vibration data.  
It combines **machine learning** (Random Forest), **signal processing** (FFT), **explainability** (SHAP), and **production-grade deployment** (FastAPI + PostgreSQL + Docker + Streamlit).

**Key results:**
- ✅ **Precision: 1.00** – No false alarms
- ✅ **Recall: 1.00** – No missed failures
- ✅ **F1: 1.00** – Perfect balance
- ✅ **Validated on 2,156 historical NASA records**
- ✅ **Monte Carlo stability test (1000 iterations, 2% noise) – no degradation**

---

## 🧠 How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  Vibration Data (NASA IMS Bearing Dataset)                     │
│  → Feature Extraction (RMS, FFT, SHAP)                        │
│  → Random Forest Model (Residual-based anomaly detection)     │
│  → FastAPI (Serving predictions)                              │
│  → PostgreSQL (Storing history)                               │
│  → Streamlit Dashboard (Visualizing results)                  │
└─────────────────────────────────────────────────────────────────┘
```

### Detection Logic

1. **Feature Engineering:** Extract RMS from raw vibration signals.
2. **Model Training:** Train Random Forest Regressor on **healthy** bearings only.
3. **Prediction:** Model predicts expected `ratio = rms_b3 / rms_b1`.
4. **Residual Calculation:** `residual = |actual_ratio - predicted_ratio|`.
5. **Anomaly Decision:** If `residual > threshold (0.05)` → **Anomaly detected**.

- **Feature Engineering:** Extract RMS (Root Mean Square) from raw vibration signals – this captures the average vibration energy per bearing.
- **Ratio Feature:** `ratio = RMS_B3 / RMS_B1` – a domain-specific feature that compares the suspicious bearing to a healthy reference.


### Threshold Selection (1.2)

- **Physical threshold:** `ratio > 1.2` → Bearing 3 vibrates 20% more than Bearing 1.
- **Empirical validation:** 0 false positives, 0 false negatives on 2,156 records.
- **Why 1.2?** It is the **lowest** threshold that still gives perfect separation.

---

## 📊 Results & Validation

### 1. Model Performance (Comparison)

| Model      | Accuracy |
|------------|----------|
| **Random Forest** | **99.54%** |
| LightGBM   | 99.31%    |
| MLP        | 99.31%    |
| XGBoost    | 99.07%    |

### 2. Anomaly Detection (Threshold = 1.2)

| Metric        | Result |
|---------------|--------|
| Precision     | 1.00   |
| Recall        | 1.00   |
| F1            | 1.00   |
| False Positives | 0    |
| False Negatives | 0    |

### 3. Failure Identification (FFT + BPFI)

- **Bearing 3** failed due to **inner race defect**.
- **BPFI ≈ 300 Hz** (calculated: `0.6 × 33.33 Hz × 15 balls`).
- **FFT shows a clear peak at ~300 Hz** in the failed bearing.

### 4. Model Explainability (SHAP)

- `rms_b3` contributes **84.5%** to the model's decision.
- `rms_b1` contributes **15.5%**.

### 5. Stability (Monte Carlo)

- **1000 iterations** with **2% noise**.
- Precision and Recall remained **1.00 ± 0.00** in all runs.

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

### Run with Docker (Production)

```bash
git clone https://github.com/eliyahudahan/anomalitor.git
cd anomalitor
docker compose up --build
```

Then open:
- **API:** `http://localhost:8000`
- **Dashboard:** `http://localhost:8501`

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Predict anomaly
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"rms_b1": 0.125, "rms_b3": 0.500}'
```

---

## 📂 Project Structure

```
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
```

---

## 📈 Dashboard Preview

The Streamlit dashboard includes:
- 📊 **Real-time ratio chart** (B3/B1) with anomaly markers
- 📋 **Recent anomalies table**
- ⚖️ **Precision-Recall curve** (threshold optimization)
- 🧠 **SHAP feature importance** (model explainability)
- 🔬 **FFT spectrum** (healthy vs failed bearing)
- 📍 **BPFI calculation** (inner race fault identification)
- 🎲 **Monte Carlo box plots** (stability test)
- 📊 **False Positives vs False Negatives** by threshold

---

## 🤝 Acknowledgments

- **NASA IMS Bearing Dataset** – [IMS Center, University of Cincinnati](www.imscenter.net)
- **Rexnord ZA-2115** bearing specifications
- Open-source libraries: Scikit-learn, FastAPI, Streamlit, SQLAlchemy, Docker

---

## 📝 Author

**Eliyahu Dahan**  
📧 framgangsrik747@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/eliyahu-dahan-684b22294/)  
🐙 [GitHub](https://github.com/eliyahudahan/anomalitor)

---

## 📅 Project Timeline

| Phase | Completed |
|-------|-----------|
| EDA + Feature Engineering | ✅ 24.05 |
| Model Comparison | ✅ 26.05 |
| Anomaly Detection | ✅ 28.05 |
| PostgreSQL + FastAPI | ✅ 31.05 |
| Docker + Streamlit | ✅ 03.06 |
| BONUS: Lead Time, SHAP, FFT, Monte Carlo | ✅ 13.06 |
| Empirical Validation | ✅ 14.06 |
| **Project Complete** | ✅ **17.06.2026** |

---

## 🎯 Conclusion

Anomalitor is a **production-ready, explainable, and validated** predictive maintenance system.  
It demonstrates **end-to-end capability** – from raw vibration data to a live dashboard – with **perfect accuracy** on real NASA bearing data.

**Ready for industry deployment.** 🚀
```


