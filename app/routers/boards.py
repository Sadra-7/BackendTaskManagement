# app/routers/boards.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.board import Board
from app.schemas.board import BoardCreate, Board as BoardSchema
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/boards", tags=["boards"])

@router.get("/", response_model=list[BoardSchema])
def get_boards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Board).filter(Board.owner_id == current_user.id).all()

@router.post("/", response_model=BoardSchema)
def create_board(board_in: BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # =======================
    # دیباگ برای بررسی داده ورودی
    # =======================
    print(f"Creating board: {board_in.title} for user {current_user.id}")

    new_board = Board(title=board_in.title, owner_id=current_user.id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board