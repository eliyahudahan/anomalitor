from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BearingRecord(Base):
    __tablename__ = "bearing_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String(30), nullable=False, index=True)
    rms_b1 = Column(Float, nullable=False)
    rms_b3 = Column(Float, nullable=False)
    ratio = Column(Float, nullable=False)
    is_anomaly = Column(Integer, default=0)
    
    predicted_ratio = Column(Float, nullable=True)
    residual = Column(Float, nullable=True)
    detected_anomaly = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
