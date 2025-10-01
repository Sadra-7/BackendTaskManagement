# app/crud/board_crud.py
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.board import Board

# گرفتن همه بردهای یک ورک‌اسپیس
def get_boards_by_workspace(db: Session, workspace_id: int) -> List[Board]:
    return db.query(Board).filter(Board.workspace_id == workspace_id).all()

# ساخت برد جدید در یک ورک‌اسپیس
def create_board(db: Session, title: str, owner_id: int, workspace_id: int) -> Board:
    board = Board(title=title, owner_id=owner_id, workspace_id=workspace_id)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board

# ویرایش برد
def update_board(db: Session, board_id: int, title: str) -> Optional[Board]:
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        return None
    board.title = title
    db.commit()
    db.refresh(board)
    return board

# حذف برد
def delete_board(db: Session, board_id: int) -> Optional[Board]:
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        return None
    db.delete(board)
    db.commit()
    return board

# گرفتن یک برد مشخص
def get_board(db: Session, board_id: int) -> Optional[Board]:
    return db.query(Board).filter(Board.id == board_id).first()