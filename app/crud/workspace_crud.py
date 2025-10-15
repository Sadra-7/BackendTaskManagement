# app/crud/workspace_crud.py
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.models.workspace import Workspace
from app.models.board import Board
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate

# -----------------------
# ایجاد ورک‌اسپیس جدید
# -----------------------
def create_workspace(db: Session, user_id: int, data: WorkspaceCreate) -> Workspace:
    # Check if workspace with same name already exists for this user
    existing_workspace = db.query(Workspace).filter(
        Workspace.name == data.name,
        Workspace.owner_id == user_id
    ).first()
    
    if existing_workspace:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail=f"A workspace with the name '{data.name}' already exists. Please choose a different name."
        )
    
    ws = Workspace(name=data.name, owner_id=user_id)
    db.add(ws)
    db.commit()
    db.refresh(ws)
    return ws

# -----------------------
# گرفتن همه ورک‌اسپیس‌های یک کاربر
# -----------------------
def get_user_workspaces(db: Session, user_id: int):
    return db.query(Workspace).filter(Workspace.owner_id == user_id).all()

# -----------------------
# گرفتن یک ورک‌اسپیس به همراه بردهایش
# -----------------------
def get_workspace(db: Session, workspace_id: int) -> Optional[Workspace]:
    return (
        db.query(Workspace)
        .options(joinedload(Workspace.boards))  # لود کردن بردها
        .filter(Workspace.id == workspace_id)
        .first()
    )

# -----------------------
# ویرایش ورک‌اسپیس
# -----------------------
def update_workspace(db: Session, workspace_id: int, data: WorkspaceUpdate) -> Optional[Workspace]:
    ws = get_workspace(db, workspace_id)
    if not ws:
        return None
    if data.name:
        # Check if another workspace with same name already exists for this user
        existing_workspace = db.query(Workspace).filter(
            Workspace.name == data.name,
            Workspace.owner_id == ws.owner_id,
            Workspace.id != workspace_id  # Exclude current workspace from check
        ).first()
        
        if existing_workspace:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail=f"A workspace with the name '{data.name}' already exists. Please choose a different name."
            )
        
        ws.name = data.name
    db.commit()
    db.refresh(ws)
    return ws

# -----------------------
# حذف ورک‌اسپیس و بردهایش
# -----------------------
def delete_workspace(db: Session, workspace_id: int) -> Optional[Workspace]:
    ws = get_workspace(db, workspace_id)
    if not ws:
        return None
    db.delete(ws)  # با cascade، بردهای مرتبط هم حذف می‌شوند
    db.commit()
    return ws

# -----------------------
# ایجاد برد جدید در یک ورک‌اسپیس
# -----------------------
def create_board_in_workspace(db: Session, workspace_id: int, title: str, owner_id: int) -> Board:
    ws = get_workspace(db, workspace_id)
    if not ws:
        return None
    board = Board(title=title, owner_id=owner_id, workspace_id=workspace_id)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board