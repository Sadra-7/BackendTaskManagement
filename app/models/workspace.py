from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    boards = relationship("Board", back_populates="workspace", cascade="all, delete-orphan")
    owner = relationship("User", back_populates="workspaces")