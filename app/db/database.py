# app/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "local")
# اگر ENV=local یا DATABASE_URL تعریف نشده باشد، از sqlite محلی استفاده می‌کنیم
if ENV == "local":
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task_manager.db")
else:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URL:
        raise ValueError("DATABASE_URL must be set in production environment")

connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # sqlite نیاز به این گزینه دارد
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()