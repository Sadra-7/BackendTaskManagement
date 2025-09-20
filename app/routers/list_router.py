from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List as TypingList
from app.db.database import get_db
from app.schemas import list as list_schema
from app.crud import list_crud
from app.models.board import Board
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/boards/{board_id}/lists", tags=["lists"])

def _ensure_board_and_owner(db: Session, board_id: int, current_user: User):
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found or access denied")
    return board

@router.get("/", response_model=TypingList[list_schema.List])
def read_lists(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _ensure_board_and_owner(db, board_id, current_user)
    return list_crud.get_lists(db, board_id=board_id)

@router.post("/", response_model=list_schema.List)
def create_list(board_id: int, list_in: list_schema.ListCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _ensure_board_and_owner(db, board_id, current_user)
    return list_crud.create_list(db, board_id=board_id, list_in=list_in)

@router.patch("/{list_id}", response_model=list_schema.List)
def update_list(board_id: int, list_id: int, list_update: list_schema.ListUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _ensure_board_and_owner(db, board_id, current_user)
    db_list = list_crud.update_list(db, list_id=list_id, title=list_update.title, color=list_update.color)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    return db_list

@router.delete("/{list_id}", response_model=list_schema.List)
def delete_list(board_id: int, list_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _ensure_board_and_owner(db, board_id, current_user)
    db_list = list_crud.delete_list(db, list_id=list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    return db_list

# ----------------------
# Cards inside list
# ----------------------
@router.post("/{list_id}/cards", response_model=list_schema.Card)
def add_card(board_id: int, list_id: int, card_in: list_schema.CardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _ensure_board_and_owner(db, board_id, current_user)
    return list_crud.add_card(db, list_id=list_id, card_in=card_in)

@router.patch("/{list_id}/cards/{card_id}", response_model=list_schema.Card)
def update_card(board_id: int, list_id: int, card_id: int, card_update: list_schema.CardUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _ensure_board_and_owner(db, board_id, current_user)
    db_card = list_crud.update_card(db, list_id=list_id, card_id=card_id, text=card_update.text, new_list_id=getattr(card_update, "list_id", None))
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@router.delete("/{list_id}/cards/{card_id}", response_model=list_schema.Card)
def delete_card(board_id: int, list_id: int, card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _ensure_board_and_owner(db, board_id, current_user)
    db_card = list_crud.delete_card(db, list_id=list_id, card_id=card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card