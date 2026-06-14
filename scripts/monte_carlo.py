import numpy as np
import pandas as pd
import psycopg2
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support

# התחבר ל-DB
conn = psycopg2.connect(
    host="db",
    database="anomalitor_db",
    user="framg",
    password=os.getenv("DB_PASSWORD", "your_password")
)
df = pd.read_sql("SELECT rms_b1, rms_b3, ratio, is_anomaly FROM bearing_records", conn)
conn.close()

print(f"Loaded {len(df)} records")

# פרמטרים
n_iter = 1000
precisions = []
recalls = []

for i in range(n_iter):
    # הוסף רעש ל-rms_b3 (2% רעש יחסי)
    noise_std = 0.02 * df['rms_b3'].std()
    noise = np.random.normal(0, noise_std, len(df))
    rms_b3_noisy = df['rms_b3'] + noise
    
    # חשב ratio חדש
    ratio_noisy = rms_b3_noisy / df['rms_b1']
    
    # threshold = 1.2
    detected = (ratio_noisy > 1.2).astype(int)
    
    # חשב Precision, Recall
    p, r, _, _ = precision_recall_fscore_support(df['is_anomaly'], detected, average='binary', zero_division=0)
    precisions.append(p)
    recalls.append(r)
    
    if (i+1) % 200 == 0:
        print(f"Completed {i+1}/{n_iter} iterations")

# Box Plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
ax1.boxplot(precisions)
ax1.set_title('Precision Distribution')
ax1.set_ylabel('Precision')
ax1.set_ylim(0, 1)
ax2.boxplot(recalls)
ax2.set_title('Recall Distribution')
ax2.set_ylabel('Recall')
ax2.set_ylim(0, 1)
plt.suptitle('Monte Carlo Simulation (1000 iterations, 2% noise)')
plt.savefig('monte_carlo_boxplots.png', dpi=150)
plt.close()

print(f"\n✅ Monte Carlo completed.")
print(f"Mean Precision: {np.mean(precisions):.3f} +/- {np.std(precisions):.3f}")
print(f"Mean Recall: {np.mean(recalls):.3f} +/- {np.std(recalls):.3f}")
print(f"Min Precision: {np.min(precisions):.3f}, Max: {np.max(precisions):.3f}")
print(f"Min Recall: {np.min(recalls):.3f}, Max: {np.max(recalls):.3f}")
