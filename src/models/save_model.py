import sys
from pathlib import Path
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

sys.path.append(str(Path(__file__).parent.parent.parent))

# טען את הנתונים
df = pd.read_csv("/home/framg/dev/anomalitor/data/nasa/processed/set1_features.csv")
df['is_anomaly'] = (df['ratio'] > 1.2).astype(int)

# אמן מודל רק על נתונים תקינים (is_anomaly == 0)
df_normal = df[df['is_anomaly'] == 0]
X = df_normal[['rms_b1', 'rms_b3']]
y = df_normal['ratio']

model = RandomForestRegressor(n_estimators=25, random_state=42)
model.fit(X, y)

# שמור את המודל
model_path = Path("/home/framg/dev/anomalitor/models/rf_residual.pkl")
model_path.parent.mkdir(parents=True, exist_ok=True)

with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Model saved to {model_path}")
print(f"Train R²: {model.score(X, y):.4f}")
