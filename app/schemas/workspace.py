from typing import List, Optional
from pydantic import BaseModel

# -----------------------
# Base Schema
# -----------------------
class WorkspaceBase(BaseModel):
    name: str


# -----------------------
# Create & Update
# -----------------------
class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None


# -----------------------
# Response
# -----------------------
class WorkspaceResponse(WorkspaceBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True   # به جای orm_mode در Pydantic v2


# -----------------------
# Workspace with Boards
# -----------------------
class BoardInWorkspace(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class WorkspaceWithBoards(WorkspaceResponse):
    boards: List[BoardInWorkspace] = []