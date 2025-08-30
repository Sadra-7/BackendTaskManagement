from pydantic import BaseModel
from typing import List

class CardBase(BaseModel):
    text: str

class CardCreate(CardBase):
    pass

class Card(CardBase):
    id : int
    class Config:
        orm_mode = True

class ListBase(BaseModel):
    title: str

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int
    cards: List[Card] = []
    class Config:
        orm_mode = True