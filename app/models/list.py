from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"))  
    user = relationship("User", back_populates="lists")  
    color = Column(String , default="#ffffff")
    cards = relationship(
        "Card",
        back_populates="list",
        cascade="all, delete-orphan"
    )