from pydantic import BaseModel

class CardBase(BaseModel):
    text: str

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    text: str

class Card(CardBase):
    id: int
    list_id: int

    class Config:
        orm_mode = True