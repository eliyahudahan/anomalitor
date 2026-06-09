# Anomalitor – Insights (תובנות מלאות)

## 25.05.2026 – Model Comparison

### מה עשיתי
- אימנתי 4 מודלים על NASA IMS Bearing Dataset:
  Random Forest, MLP, XGBoost, LightGBM.
  כל מודל מאמן את עצמו אחרת, כאשר הוא לומד מ-80% מהנתונים, 
  על ה-20% הנותרים הוא נבחן בלי לראות את התשובות.
  תוצאות המבחן נקבעות על פי המחקר של נאס"א ועל פי הספים שקבעתי בסיוע AI.
- השתמשתי ב-3 פיצ'רים: rms_b1, rms_b3, ratio.
- הגדרתי 3 שלבי שחיקה לפי ratio: Healthy (<1.2), Early (1.2-2.0), Failure (>=2.0). השלבים הללו הם הספים.

### תוצאות
- Random Forest: **99.54% Accuracy** – ניצח.
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

---

## 27.05.2026 – Anomaly Detection

- הגדרתי סף חריגה פיזיקלי: `ratio > 1.2`.
- אימנתי Random Forest Regressor על נתונים תקינים בלבד (R² = 0.995).
- `residual = |actual - predicted|`.
- `threshold` = 95th percentile of residuals (normal data).
- תוצאות:
  - **recall = 1.00** – זיהינו את כל החריגים.
  - **precision = 0.27** – הרבה אזעקות שווא.
  - **F1 = 0.43** – נמוך בגלל precision, אבל ב-Predictive Maintenance מעדיפים אזעקת שווא על פני החמצת כשל.

---

## 31.05.2026 – FastAPI + PostgreSQL Integration

### API Endpoints
- `GET /health` – בדיקת בריאות השרת.
- `POST /predict` – מקבל `{"rms_b1": float, "rms_b3": float}`, מחזיר `actual_ratio`, `predicted_ratio`, `residual`, `is_anomaly`.

### Database
- טבלה: `bearing_records`.
- עמודות: `id`, `timestamp`, `rms_b1`, `rms_b3`, `ratio`, `is_anomaly`, `predicted_ratio`, `residual`, `detected_anomaly`, `created_at`.
- כל חיזוי נשמר ב-DB עם שעת הקבלה.

### Test
- `curl` request → 200 OK, DB row added.

---

## 01.06.2026 – הבנת הקבצים הפנימיים

### `src/database/config.py`
- **engine**: מנהל חיבורים ל-DB (connection pool).
- **SessionLocal**: מפעל ליצירת Sessions (עסקאות).
- **get_db**: Dependency Injection – יוצר Session, מחזיר לפונקציה, וסוגר בסוף.
- **yield**: מחזיר ערך, מאפשר לחזור לפונקציה אחרי שהיא מסתיימת (ניהול משאבים).

### `src/database/models.py`
- **Base = declarative_base()**: מחלקת בסיס שאוספת את הגדרות הטבלאות.
- **`__tablename__`**: שם הטבלה ב-DB.
- **Column**: מגדיר עמודה.
- **Integer, String, Float, DateTime**: סוגי הנתונים.
- **nullable=False**: חובה למלא.
- **default**: ברירת מחדל.

### `src/database/create_tables.py`
- `Base.metadata.create_all(bind=engine)` – יוצר את הטבלאות ב-DB לפי ההגדרות ב-models.

### `src/database/insert_data.py`
- קורא את `set1_features.csv` (pandas).
- יוצר `is_anomaly` לפי `ratio > 1.2`.
- `with Session(engine) as session` – מנהל session אוטומטית (נסגר בסוף).
- `session.add(record)` – מוסיף שורה בזיכרון.
- `session.commit()` – שומר את כל השינויים ל-DB.

### `src/models/save_model.py`
- מאמן Random Forest על נתונים תקינים בלבד (`is_anomaly == 0`).
- `pickle.dump(model, file)` – שומר את המודל לדיסק (קובץ בינארי).

### `app/main.py`
- טוען את המודל (`pickle.load`).
- מגדיר FastAPI עם endpoints.
- `/predict`:
  - ממיר JSON למערך NumPy.
  - מפעיל `model.predict`.
  - מחשב `actual_ratio`, `residual`, `is_anomaly`.
  - שומר את התוצאה ל-DB.
  - מחזיר JSON.

---

## 02.06.2026 – Docker

### הישגים
- כתבתי `Dockerfile` ו-`docker-compose.yml`.
- הוספתי `.dockerignore` (הפחית את context מ-9GB ל-5MB).
- תיקנתי בעיית פורט 5432 (עצרתי PostgreSQL מקומי).
- הוספתי `python-dotenv` ל-`requirements.txt` (חבילה שחסרה בקונטיינר).
- הרצתי `docker-compose up --build` – שני הקונטיינרים (`db` ו-`api`) עולים ורצים.

### המנטרה
> *`Base` – אוסף תוכניות.  
> `engine` – המהנדס.  
> `Session` – העיפרון.  
> `commit` – החתימה.  
> `docker-compose up` – מרים הכל.*

---

## אבני דרך עיקריות (סיכום)

| תאריך | אבן דרך |
|--------|----------|
| 25.05 | השוואת מודלים – RF ניצח (99.54%) |
| 27.05 | Anomaly Detection (recall=1.00) |
| 31.05 | FastAPI + PostgreSQL – API חי |
| 01.06 | הבנת כל מודולי התשתית (config, models, create_tables, insert_data, save_model, main) |
| 02.06 | Docker – כל המערכת רצה ב-`docker-compose up` |

---

**סוף התובנות (נכון ל-02.06.2026, שעה 13:00).**

07.06.2026 – Streamlit Dashboard
יצרתי dashboard.py עם Streamlit.

חיבור ל-DB: psycopg2.connect(host="db", database="anomalitor_db", user="framg", password=...)

קריאת נתונים: pd.read_sql("SELECT * FROM bearing_records", conn)

גרף: px.line(df, x='timestamp', y='ratio', color='detected_anomaly') – קו כחול (תקין), קו אדום (אנומליה).

כרטיסים: st.metric("Total Predictions", len(df)) ו-st.metric("Anomalies Detected", len(anomalies)).

07.06.2026 – entrypoint.sh
#!/bin/sh – מגדיר shell.

set -e – עוצר על שגיאה.

sleep 5 – מחכה שה-DB יעלה.

python -c "from src.database.config import engine; from src.database.models import Base; Base.metadata.create_all(bind=engine)" – יוצר טבלאות.

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 – מפעיל את FastAPI (מחליף תהליך).

08.06-09.06.2026 – הבנת FastAPI ו-Pydantic
FastAPI – מסגרת לבניית API. מגדיר endpoints (@app.post("/predict")), מנתב בקשות, מפעיל פונקציות.

Pydantic – ספרייה לבדיקת JSON. מגדיר תבנית (class BearingData(BaseModel)). FastAPI משתמש בה אוטומטית.

Uvicorn – שרת רשת. טוען את FastAPI (app.main:app) ומפעיל אותו.

curl – כלי לשליחת בקשות HTTP מהטרמינל. מדמה לקוח, בודק API, שולח נתונים.

08.06-09.06.2026 – הבנת docker-compose.yml
שירות db: PostgreSQL, עם healthcheck ו-volumes.

שירות api: FastAPI, רץ באמצעות entrypoint.sh, תלוי ב-db (service_healthy).

שירות streamlit: Dashboard, רץ עם Streamlit, תלוי ב-api.

רשת Docker: כל שירות יכול לפנות לאחר בשם השירות (למשל host="db").

ports: חושף פורט מהקונטיינר למחשב המארח (למשל 8000:8000).

environment: מעביר משתני סביבה (מ-.env).

📊 אבני דרך מעודכנות (נכון ל-09.06)
תאריך	אבן דרך
25.05	השוואת מודלים – RF ניצח (99.54%)
27.05	Anomaly Detection (recall=1.00)
31.05	FastAPI + PostgreSQL – API חי
01.06	הבנת מודולי התשתית
02.06	Docker – docker-compose up
07.06	Streamlit Dashboard + entrypoint.sh
08-09.06	הבנת FastAPI, Pydantic, Uvicorn, curl, docker-compose.yml

