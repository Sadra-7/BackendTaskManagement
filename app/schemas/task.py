
from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    column_id: Optional[int] = None

class TaskCreate(TaskBase):
    status: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    column_id: Optional[int] = None

class TaskList(BaseModel):
    tasks: List[TaskCreate]

class TaskOut(TaskCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
        
class ColumnBase(BaseModel):
    title: str

class ColumnCreate(ColumnBase):
    pass

class ColumnOut(ColumnBase):
    id: int
    tasks: List[TaskOut] = []

    class Config:
        from_attributes = True




