from pydantic import BaseModel

class BoardBase(BaseModel):
    title: str

class BoardCreate(BoardBase):
    pass

class Board(BoardBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True