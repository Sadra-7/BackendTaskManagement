from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Label(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    color = Column(String, default="#000000")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="labels")
    tasks = relationship("Task", back_populates="label")