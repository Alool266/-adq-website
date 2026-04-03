from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Supabase connection
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://kepyyudsrfhofseownnj.supabase.co")
SUPABASE_PASSWORD = os.environ.get("SUPABASE_PASSWORD", "sWie0KkZwQ2V231p")

# Use Supabase PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{SUPABASE_PASSWORD}@db.kepyyudsrfhofseownnj.supabase.co:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
