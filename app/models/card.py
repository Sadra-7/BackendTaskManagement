from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    list_id = Column(Integer, ForeignKey("lists.id")) 
    list = relationship("List", back_populates="cards")