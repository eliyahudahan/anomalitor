import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# נתיב לקובץ TSV (בחר קובץ תקין ואחד עם כשל)
healthy_file = "/app/data/raw/1st_test/1st_test/2003.10.22.12.06.24"  # תחילת הניסוי
failed_file = "/app/data/raw/1st_test/1st_test/2003.11.25.23.39.56"   # כשל

def load_bearing_data(file_path):
    """טען קובץ TSV עם 8 עמודות"""
    df = pd.read_csv(file_path, sep='\t', header=None,
                     names=["B1_X", "B1_Y", "B2_X", "B2_Y",
                            "B3_X", "B3_Y", "B4_X", "B4_Y"])
    return df

def plot_fft(signal, fs=20000, title="FFT Spectrum"):
    """חשב והצג FFT של האות"""
    n = len(signal)
    yf = fft(signal)
    xf = fftfreq(n, 1/fs)[:n//2]
    
    plt.figure(figsize=(12,4))
    plt.plot(xf, 2.0/n * np.abs(yf[:n//2]))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.grid(True)
    return plt

# טען קבצים
df_healthy = load_bearing_data(healthy_file)
df_failed = load_bearing_data(failed_file)

# קח את B3_X (מיסב 3 שיכשל)
signal_healthy = df_healthy['B3_X'].values
signal_failed = df_failed['B3_X'].values

# חשב FFT
plt1 = plot_fft(signal_healthy, title="Bearing 3 - Healthy (Start)")
plt1.savefig('/app/fft_healthy.png')
plt1.close()

plt2 = plot_fft(signal_failed, title="Bearing 3 - Failed (End)")
plt2.savefig('/app/fft_failed.png')
plt2.close()

print("✅ FFT analysis complete.")
print("Graphs saved: fft_healthy.png, fft_failed.png")