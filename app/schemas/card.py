from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class CardBase(BaseModel):
    text: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    members: List[str] = []
    attachments: List[str] = []

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardResponse(CardBase):
    id: int
    list_id: int
    position: int

    class Config:
        orm_mode = True