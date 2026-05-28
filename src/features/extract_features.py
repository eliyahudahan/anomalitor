import os
import pandas as pd
import numpy as np
from pathlib import Path

def extract_rms_from_file(file_path):
    """מקבל נתיב לקובץ TSV, מחזיר RMS של B1_X ו-B3_X"""
    df = pd.read_csv(file_path, sep='\t', header=None,
                     names=["B1_X", "B1_Y", "B2_X", "B2_Y",
                            "B3_X", "B3_Y", "B4_X", "B4_Y"])
    
    rms_b1 = np.sqrt(np.mean(df["B1_X"]**2))
    rms_b3 = np.sqrt(np.mean(df["B3_X"]**2))
    
    return rms_b1, rms_b3

def extract_timestamp_from_filename(filename):
    """מחלץ תאריך ושעה משם הקובץ (למשל: 2003.10.22.12.06.24)"""
    base = os.path.basename(filename)
    # מפרידים לפי נקודות
    parts = base.split('.')
    if len(parts) == 5:
        year, month, day, hour, minute_second = parts
        minute = minute_second[:2]
        second = minute_second[2:]
        return f"{year}-{month}-{day} {hour}:{minute}:{second}"
    return base

def process_all_files(data_folder):
    """עובר על כל הקבצים בתיקייה, מחזיר DataFrame עם RMS ו-timestamp"""
    results = []
    files = sorted(Path(data_folder).glob("*"))
    
    for file_path in files:
        if file_path.name.startswith("2003"):  # רק קבצי נתונים
            rms_b1, rms_b3 = extract_rms_from_file(file_path)
            timestamp = extract_timestamp_from_filename(file_path.name)
            
            results.append({
                'timestamp': timestamp,
                'rms_b1': rms_b1,
                'rms_b3': rms_b3,
                'ratio': rms_b3 / rms_b1
            })
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    # הרצה ישירה – יוצרת את הקובץ המעובד
    data_folder = "/home/framg/dev/anomalitor/data/nasa/raw/1st_test/1st_test"
    df_features = process_all_files(data_folder)
    
    # שמירה
    output_path = "/home/framg/dev/anomalitor/data/nasa/processed/set1_features.csv"
    df_features.to_csv(output_path, index=False)
    print(f"Saved {len(df_features)} records to {output_path}")