# Anomalitor – Insights

## 25.05.2026 – Model Comparison

### מה עשיתי
- אימנתי 4 מודלים על NASA IMS Bearing Dataset:
  Random Forest, MLP, XGBoost, LightGBM.
  כל מודל מאמן את עצמו אחרת, כאשר הוא לומד מ80% מהנתונים, 
  על ה20% נותרים הוא נבחן בלי לראות את התשובות
  תוצאות המבחן נקבעות על פי המחקר של נאס"א ועל פי הספים שקבעתי בסיוע AI
- השתמשתי ב-3 פיצ'רים: rms_b1, rms_b3, ratio.
- הגדרתי 3 שלבי שחיקה לפי ratio: Healthy (<1.2), Early (1.2-2.0), Failure (>=2.0). השלבים הללו הם הספים.

### תוצאות
- Random Forest: 99.54% Accuracy – ניצח.
- LightGBM: 99.31%.
- MLP: 99.31% (אבל לא זיהה Failure).
- XGBoost: 99.07%.

### מסקנה
המאמר טען ש-MLP ינצח. בניסוי שלי – RF ניצח.
RF פשוט יותר, מהיר יותר, והתמודד טוב עם הדאטה הלא מאוזן.

### מה הלאה
- Anomaly Detection: anomaly_score + threshold.
- PostgreSQL.
- FastAPI.

### 27.05.2026 – Anomaly Detection

- הגדרתי סף חריגה פיזיקלי: ratio > 1.2.
- אימנתי Random Forest Regressor על נתונים תקינים בלבד (R² = 0.995).
- residual = |actual - predicted|.
- threshold = 95th percentile of residuals (normal data).
- תוצאות: recall = 1.00 (זיהינו את כל החריגים), precision = 0.27 (הרבה אזעקות שווא).
- F1 = 0.43 – נמוך בגלל ה-precision הנמוך, אבל ב-Predictive Maintenance מעדיפים אזעקת שווא על פני החמצת כשל.