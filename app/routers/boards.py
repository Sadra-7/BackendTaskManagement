# app/routers/boards.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate, Board as BoardSchema
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/boards", tags=["Boards"])

# -----------------------
# دریافت بردها بر اساس ورک‌اسپیس
# -----------------------
@router.get("/", response_model=List[BoardSchema])
def get_boards(
    workspace_id: int = Query(..., description="شناسه ورک‌اسپیس برای فیلتر بردها"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    دریافت همه بردهای متعلق به کاربر در یک ورک‌اسپیس مشخص
    """
    boards = (
        db.query(Board)
        .filter(Board.owner_id == current_user.id, Board.workspace_id == workspace_id)
        .all()
    )
    return boards

# -----------------------
# ایجاد برد جدید در یک ورک‌اسپیس
# -----------------------
@router.post("/", response_model=BoardSchema)
def create_board(
    board_in: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ایجاد یک برد جدید تحت ورک‌اسپیس مشخص
    """
    if not hasattr(board_in, "workspace_id") or board_in.workspace_id is None:
        raise HTTPException(status_code=400, detail="workspace_id باید مشخص شود")
    
    new_board = Board(
        title=board_in.title,
        owner_id=current_user.id,
        workspace_id=board_in.workspace_id
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

# -----------------------
# ویرایش برد
# -----------------------
@router.put("/{board_id}", response_model=BoardSchema)
def update_board(
    board_id: int,
    board_in: BoardUpdate,  # فقط عنوان لازم است
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ویرایش عنوان یک برد
    """
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    board.title = board_in.title
    db.commit()
    db.refresh(board)
    return board

# -----------------------
# حذف برد
# -----------------------
@router.delete("/{board_id}", status_code=204)
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    حذف یک برد مشخص
    """
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    db.delete(board)
    db.commit()
    return None