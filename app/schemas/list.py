from pydantic import BaseModel
from typing import List as TypingList, Optional
from datetime import date

class CardBase(BaseModel):
    text: str

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class Card(CardBase):
    id: int
    list_id: int
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    position: int = 0
    members: Optional[list] = []
    attachments: Optional[list] = []

    class Config:
        orm_mode = True

class ListBase(BaseModel):
    title: str
    color: Optional[str] = "#ffffff"

class ListCreate(ListBase):
    pass

class ListUpdate(BaseModel):
    title: Optional[str] = None
    color: Optional[str] = None

class List(ListBase):
    id: int
    cards: TypingList[Card] = []

    class Config:
        orm_mode = True

class CardUpdatePosition(BaseModel):
    new_list_id: int
    new_position: int