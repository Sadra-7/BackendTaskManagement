from __future__ import annotations
import secrets
from datetime import datetime, timedelta
import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum, Index, text
from sqlalchemy.orm import relationship
from app.db.database import Base

class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    number = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)
    reset_password_token = Column(String(128), nullable=True, unique=True)
    reset_password_expire = Column(DateTime, nullable=True)

    boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")
    lists = relationship("List", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user")

    __table_args__ = (
        Index(
            "uq_users_number",
            "number",
            unique=True,
            mssql_where=text("number IS NOT NULL")
        ),
    )

    def generate_reset_token(self):
        self.reset_password_token = secrets.token_urlsafe(32)
        self.reset_password_expire = datetime.utcnow() + timedelta(minutes=15)