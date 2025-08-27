from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.label import LabelOut  # فرضی، اگر وجود دارد

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    column_id: Optional[int] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    label_id: Optional[int] = None

class TaskCreate(TaskBase):
    status: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    column_id: Optional[int] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    label_id: Optional[int] = None

class TaskList(BaseModel):
    tasks: List[TaskCreate]

class TaskOut(BaseModel):
    id: int
    title: str
    status: str
    startDate: Optional[datetime]  # اصلاح شده به datetime
    endDate: Optional[datetime]    # اصلاح شده به datetime
    label: Optional[LabelOut] = None

    class Config:
        orm_mode = True

class ColumnBase(BaseModel):
    title: str

class ColumnCreate(ColumnBase):
    pass

class ColumnOut(ColumnBase):
    id: int
    tasks: List[TaskOut] = []

    class Config:
        orm_mode = True