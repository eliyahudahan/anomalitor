#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.config import engine
from src.database.models import Base

def create_tables():
    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully:")
    for table in Base.metadata.tables.keys():
        print(f"   - {table}")

if __name__ == "__main__":
    create_tables()
