from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.crud import card_crud
from app.schemas.card import Card, CardCreate, CardUpdate

router = APIRouter(prefix="/lists/{list_id}/cards", tags=["Cards"])

# -------------------------
# ایجاد کارت جدید
# -------------------------
@router.post("/", response_model=Card)
def create_card_endpoint(list_id: int, card: CardCreate, db: Session = Depends(get_db)):
    return card_crud.create_card(db, card, list_id)

# -------------------------
# گرفتن همه کارت‌ها
# -------------------------
@router.get("/", response_model=List[Card])
def get_cards_endpoint(list_id: int, db: Session = Depends(get_db)):
    return card_crud.get_cards_by_list(db, list_id)

# -------------------------
# آپدیت متن کارت
# -------------------------
@router.put("/{card_id}", response_model=Card)
def update_card_endpoint(list_id: int, card_id: int, update: CardUpdate, db: Session = Depends(get_db)):
    card = card_crud.update_card(db, card_id, update.text)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

# -------------------------
# حذف کارت
# -------------------------
@router.delete("/{card_id}")
def delete_card_endpoint(list_id: int, card_id: int, db: Session = Depends(get_db)):
    success = card_crud.delete_card(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Card deleted successfully ✅"}

# -------------------------
# 🟢 مسیر جدید برای Drag & Drop
# -------------------------
@router.patch("/{card_id}/move", response_model=Card)
def move_card_endpoint(
    list_id: int,
    card_id: int,
    new_list_id: int = Query(..., description="ID of the list to move the card into"),
    new_position: int = Query(..., description="Index position in the new list"),
    db: Session = Depends(get_db)
):
    """
    تغییر لیست و موقعیت کارت. 
    new_list_id: آی‌دی لیست مقصد
    new_position: جایگاه کارت در لیست مقصد (0-indexed)
    """
    card = card_crud.move_card(db, card_id, new_list_id, new_position)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card