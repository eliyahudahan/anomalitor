#!/bin/sh
echo "Waiting for PostgreSQL to be ready..."
sleep 5
echo "Creating tables..."
python -c "from src.database.config import engine; from src.database.models import Base; Base.metadata.create_all(bind=engine)"
echo "Tables created. Starting API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000