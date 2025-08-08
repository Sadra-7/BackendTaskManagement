from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="pending")  # این خط اضافه شد
    column_id = Column(Integer, ForeignKey("columns.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    column = relationship("Column", back_populates="tasks")
    owner = relationship("User", back_populates="tasks")

class Column(Base):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    tasks = relationship("Task", back_populates="column", cascade="all, delete-orphan")
    owner = relationship("User", back_populates="columns")