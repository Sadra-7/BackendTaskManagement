from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate, WorkspaceWithBoards
from app.crud import workspace_crud

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

# ساخت ورک اسپیس جدید
@router.post("/", response_model=WorkspaceResponse)
def create_workspace(data: WorkspaceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workspace_crud.create_workspace(db, current_user.id, data)

# دریافت ورک اسپیس‌های کاربر
@router.get("/", response_model=List[WorkspaceResponse])
def get_workspaces(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workspace_crud.get_user_workspaces(db, current_user.id)

# دریافت یک ورک اسپیس با بوردها
@router.get("/{workspace_id}", response_model=WorkspaceWithBoards)
def get_workspace(workspace_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ws = workspace_crud.get_workspace(db, workspace_id)
    if not ws or ws.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return ws

# ویرایش ورک اسپیس
@router.put("/{workspace_id}", response_model=WorkspaceResponse)
def update_workspace(workspace_id: int, data: WorkspaceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ws = workspace_crud.get_workspace(db, workspace_id)
    if not ws or ws.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace_crud.update_workspace(db, workspace_id, data)

# حذف ورک اسپیس
@router.delete("/{workspace_id}")
def delete_workspace(workspace_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ws = workspace_crud.get_workspace(db, workspace_id)
    if not ws or ws.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Workspace not found")
    workspace_crud.delete_workspace(db, workspace_id)
    return {"message": "Workspace deleted successfully"}