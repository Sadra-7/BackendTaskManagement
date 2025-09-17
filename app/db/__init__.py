from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# آدرس دیتابیس SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"

# اتصال به دیتابیس
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ساخت session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base برای تعریف مدل‌ها
Base = declarative_base()