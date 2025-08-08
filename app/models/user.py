# app/models/user.py
import secrets
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
import enum
from app.db.database import Base
from sqlalchemy.orm import relationship

class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)
    reset_password_token = Column(String, nullable=True, unique=True)
    reset_password_expire = Column(DateTime, nullable=True)
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    columns = relationship("Column", back_populates="owner", cascade="all, delete-orphan")
    def generate_reset_token(self):
        self.reset_password_token = secrets.token_urlsafe(32)
        
        self.reset_password_expire = datetime.utcnow() + timedelta(minutes=15)