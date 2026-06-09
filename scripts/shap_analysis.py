import pandas as pd
import pickle
import shap
import numpy as np
import psycopg2
import os
import matplotlib
matplotlib.use('Agg')  # Backend ללא GUI
import matplotlib.pyplot as plt

# התחבר ל-DB
conn = psycopg2.connect(
    host="db",
    database="anomalitor_db",
    user="framg",
    password=os.getenv("DB_PASSWORD", "your_password")
)

# טען נתונים (רק תקינים, כמו באימון)
df = pd.read_sql("SELECT rms_b1, rms_b3, ratio, is_anomaly FROM bearing_records", conn)
conn.close()

# טען מודל
with open("/app/models/rf_residual.pkl", "rb") as f:
    model = pickle.load(f)

# השתמש ב-explainer של SHAP
X = df[['rms_b1', 'rms_b3']].values  # או df[['rms_b1', 'rms_b3', 'ratio']]
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# שמור גרף summary
shap.summary_plot(shap_values, X, feature_names=['rms_b1', 'rms_b3'], show=False)
plt.savefig('/app/shap_summary.png', bbox_inches='tight', dpi=150)
plt.close()

print("✅ SHAP analysis complete. Graph saved to /app/shap_summary.png")
print("Feature importance (model):", model.feature_importances_)