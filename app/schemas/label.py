from pydantic import BaseModel

class LabelBase(BaseModel):
    title: str
    color: str

class LabelCreate(LabelBase):
    pass

class LabelOut(LabelBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True