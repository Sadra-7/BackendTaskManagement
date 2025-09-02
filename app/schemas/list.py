from pydantic import BaseModel
from typing import List , Optional


class CardBase(BaseModel):
    text: str

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class Card(CardBase):
    id: int
    list_id: int

    class Config:
        orm_mode = True

class ListBase(BaseModel):
    title: str
    color: Optional[str] = "#ffffff"

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int
    cards: List[Card] = []
    class Config:
        orm_mode = True

class ListUpdate(BaseModel):
    title : Optional[str] = None
    color : Optional[str] = None


