import sys
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.database.config import engine
from src.database.models import BearingRecord

# טען את ה-CSV
df = pd.read_csv("/home/framg/dev/anomalitor/data/nasa/processed/set1_features.csv")
df['is_anomaly'] = (df['ratio'] > 1.2).astype(int)

# הכנס לטבלה
with Session(engine) as session:
    # מחק נתונים קיימים (אם רוצים לרוץ שוב)
    session.query(BearingRecord).delete()
    
    for _, row in df.iterrows():
        record = BearingRecord(
            timestamp=row['timestamp'],
            rms_b1=row['rms_b1'],
            rms_b3=row['rms_b3'],
            ratio=row['ratio'],
            is_anomaly=row['is_anomaly']
        )
        session.add(record)
    session.commit()
    
print(f"✅ Inserted {len(df)} records into bearing_records")
