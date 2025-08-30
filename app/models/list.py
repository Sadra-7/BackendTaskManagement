from sqlalchemy import Column , Integer , String
from sqlalchemy.orm import relationship
from app.db.database import Base

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True , index=True)
    title = Column(String , nullable = False)

    cards = relationship("Card", back_populates="list" , cascade="all,delete-orphan")