from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from app.db.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    position = Column(Integer, default=0)
    members = Column(JSON, default=[])
    attachments = Column(JSON, default=[])

    list = relationship("List", back_populates="cards")