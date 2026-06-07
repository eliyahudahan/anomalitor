from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# טעינת המודל
model_path = Path("/app/models/rf_residual.pkl")
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# חיבור ל-DB
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="Anomalitor API", description="API for bearing anomaly detection", version="1.0")

class BearingData(BaseModel):
    rms_b1: float
    rms_b3: float

@app.get("/")
def root():
    return {"message": "Anomalitor API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: BearingData):
    try:
        features = np.array([[data.rms_b1, data.rms_b3]])
        predicted_ratio = float(model.predict(features)[0])
        actual_ratio = data.rms_b3 / data.rms_b1
        residual = abs(actual_ratio - predicted_ratio)
        threshold = 0.05
        is_anomaly = residual > threshold
        
        # ← הוסף את השורה הזו
        save_prediction_to_db(data.rms_b1, data.rms_b3, actual_ratio, predicted_ratio, residual, is_anomaly)
        
        return {
            "actual_ratio": actual_ratio,
            "predicted_ratio": predicted_ratio,
            "residual": residual,
            "is_anomaly": is_anomaly
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def save_prediction_to_db(rms_b1, rms_b3, actual_ratio, predicted_ratio, residual, is_anomaly):
    from src.database.models import BearingRecord
    from src.database.config import SessionLocal
    from datetime import datetime
    
    db = SessionLocal()
    record = BearingRecord(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # ← הוסף שורה זו
        rms_b1=rms_b1,
        rms_b3=rms_b3,
        ratio=actual_ratio,
        predicted_ratio=predicted_ratio,
        residual=residual,
         is_anomaly=1 if is_anomaly else 0,   # ← תיקון! שומר גם את האמת
        detected_anomaly=1 if is_anomaly else 0
    )
    db.add(record)
    db.commit()
    db.close()