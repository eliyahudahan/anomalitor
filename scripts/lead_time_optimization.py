import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
import psycopg2
import os

# התחבר ל-DB
conn = psycopg2.connect(
    host="db",
    database="anomalitor_db",
    user="framg",
    password=os.getenv("DB_PASSWORD", "your_password")
)

# טען נתונים
df = pd.read_sql("SELECT ratio, detected_anomaly, is_anomaly FROM bearing_records", conn)

# סגור חיבור
conn.close()

# חישוב Precision-Recall עבור ספים שונים (מבוסס על residual? 
# אבל בדאטה שלך יש כבר detected_anomaly. 
# אנחנו נשתמש ב-detected_anomaly כניקוד (score) לבי"ש.

# אם אין לך ניקוד רציף, אפשר לדמות: 
# נניח שיש מתאם בין residual ל-detected_anomaly.
# בקוד שלך, detected_anomaly מחושב מ-residual > threshold.
# נבנה Precision-Recall curve על ידי שינוי threshold.

# (בפועל, היינו צריכים את הניקוד הגולמי של המודל, 
# אבל נוכל להסתפק במה שיש.)

# נניח שניקוד = residual (או ratio).
score = df['ratio'].values
y_true = df['is_anomaly'].values

# חשב precision, recall, thresholds
precision, recall, thresholds = precision_recall_curve(y_true, score)

# הצג גרף
plt.figure(figsize=(10,5))
plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.grid(True)
plt.show()

# מצא את threshold שממקסם את F1 (איזון)
f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
best_idx = np.argmax(f1_scores[:-1])  # ההתאמה לאורכים
best_threshold = thresholds[best_idx]
best_precision = precision[best_idx]
best_recall = recall[best_idx]

print(f"Best threshold (on ratio): {best_threshold:.3f}")
print(f"Precision: {best_precision:.3f}, Recall: {best_recall:.3f}")
print(f"F1-score: {f1_scores[best_idx]:.3f}")