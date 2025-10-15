from pydantic import BaseModel
from typing import Optional

class BoardBase(BaseModel):
    title: str

# برای ایجاد برد باید workspace_id هم فرستاده شود
class BoardCreate(BoardBase):
    workspace_id: int

# برای ویرایش برد فقط title را نیاز داریم
class BoardUpdate(BaseModel):
    title: str

class Board(BoardBase):
    id: int
    owner_id: int
    workspace_id: Optional[int] = None

    class Config:
        orm_mode = True