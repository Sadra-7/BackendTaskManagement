from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.card import Card, CardCreate, CardUpdate   # 👈 مستقیم ایمپورت شد
from app.crud import card_crud

router = APIRouter(
    prefix="/lists/{list_id}/cards",
    tags=["Cards"]
)

# 📌 ایجاد کارت جدید در یک لیست
@router.post("/", response_model=Card)
def create_card(list_id: int, card: CardCreate, db: Session = Depends(get_db)):
    return card_crud.create_card(db, card, list_id)

# 📌 گرفتن همه کارت‌های یک لیست
@router.get("/", response_model=List[Card])
def get_cards(list_id: int, db: Session = Depends(get_db)):
    return card_crud.get_cards_by_list(db, list_id)

# 📌 آپدیت کارت
@router.put("/{card_id}", response_model=Card)
def update_card(list_id: int, card_id: int, update: CardUpdate, db: Session = Depends(get_db)):
    card = card_crud.update_card(db, card_id, update.text)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

# 📌 حذف کارت
@router.delete("/{card_id}")
def delete_card(list_id: int, card_id: int, db: Session = Depends(get_db)):
    success = card_crud.delete_card(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Card deleted successfully ✅"}