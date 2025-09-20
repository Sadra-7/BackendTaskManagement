from pydantic import BaseModel

class CardBase(BaseModel):
    text: str

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardMove(BaseModel):
    list_id: int
    position: int

class Card(CardBase):
    id: int
    list_id: int
    position: int

    class Config:
        orm_mode = True