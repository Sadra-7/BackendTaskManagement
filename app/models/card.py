from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    position = Column(Integer, nullable=False, default=0)  # 🟢 ستون جدید برای ترتیب کارت

    list = relationship("List", back_populates="cards")