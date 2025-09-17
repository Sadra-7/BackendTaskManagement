# app/routers/boards.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.board import Board
from app.schemas.board import BoardCreate, Board as BoardSchema
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/boards", tags=["boards"])

# =======================
# دریافت تمام بردهای کاربر
# =======================
@router.get("/", response_model=list[BoardSchema])
def get_boards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Board).filter(Board.owner_id == current_user.id).all()

# =======================
# ایجاد برد جدید
# =======================
@router.post("/", response_model=BoardSchema)
def create_board(board_in: BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(f"Creating board: {board_in.title} for user {current_user.id}")
    new_board = Board(title=board_in.title, owner_id=current_user.id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

# =======================
# ویرایش برد
# =======================
@router.put("/{board_id}", response_model=BoardSchema)
def update_board(board_id: int, board_in: BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    board.title = board_in.title
    db.commit()
    db.refresh(board)
    return board

# =======================
# حذف برد
# =======================
@router.delete("/{board_id}", status_code=204)
def delete_board(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    db.delete(board)
    db.commit()
    return None