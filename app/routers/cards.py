# app/routers/cards.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List as TypingList
from app.db.database import get_db
from app.models.card import Card
from app.models.list import List as ListModel
from app.schemas.card import CardCreate, CardUpdate, CardResponse

router = APIRouter(
    tags=["Cards"]
)

# -----------------------
# دریافت همه کارت‌های یک لیست
# -----------------------
@router.get("/lists/{list_id}/cards", response_model=TypingList[CardResponse])
def get_cards_by_list(list_id: int, db: Session = Depends(get_db)):
    list_obj = db.query(ListModel).filter(ListModel.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    return list_obj.cards

# -----------------------
# ساخت کارت جدید در یک لیست مشخص
# -----------------------
@router.post("/lists/{list_id}/cards", response_model=CardResponse)
def create_card(list_id: int, card_in: CardCreate, db: Session = Depends(get_db)):
    list_obj = db.query(ListModel).filter(ListModel.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")

    last_card = db.query(Card).filter(Card.list_id == list_id).order_by(Card.position.desc()).first()
    position = last_card.position + 1 if last_card else 0

    card = Card(
        text=card_in.text,
        description=card_in.description,
        start_date=card_in.start_date,
        end_date=card_in.end_date,
        members=card_in.members,
        attachments=card_in.attachments,
        list_id=list_id,
        position=position
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

# -----------------------
# دریافت یک کارت مشخص
# -----------------------
@router.get("/cards/{card_id}", response_model=CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

# -----------------------
# آپدیت کارت بدون list_id (مسیر جدید)
# -----------------------
@router.put("/cards/{card_id}", response_model=CardResponse)
def update_card(card_id: int, card_in: CardUpdate, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card.text = card_in.text
    card.description = card_in.description
    card.start_date = card_in.start_date
    card.end_date = card_in.end_date
    card.members = card_in.members
    card.attachments = card_in.attachments

    db.commit()
    db.refresh(card)
    return card

# -----------------------
# آپدیت کارت با list_id (برای فرانت قدیمی)
# -----------------------
@router.put("/lists/{list_id}/cards/{card_id}", response_model=CardResponse)
def update_card_with_list(list_id: int, card_id: int, card_in: CardUpdate, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card.text = card_in.text
    card.description = card_in.description
    card.start_date = card_in.start_date
    card.end_date = card_in.end_date
    card.members = card_in.members
    card.attachments = card_in.attachments

    db.commit()
    db.refresh(card)
    return card

# -----------------------
# حذف کارت بدون list_id
# -----------------------
@router.delete("/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return {"detail": "Card deleted"}

# -----------------------
# حذف کارت با list_id (برای فرانت قدیمی)
# -----------------------
@router.delete("/lists/{list_id}/cards/{card_id}")
def delete_card_with_list(list_id: int, card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return {"detail": "Card deleted"}

# -----------------------
# جابجایی کارت بین لیست‌ها یا تغییر position بدون list_id
# -----------------------
@router.patch("/cards/{card_id}/move", response_model=CardResponse)
def move_card(
    card_id: int,
    new_list_id: int,
    new_position: int,
    db: Session = Depends(get_db)
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    old_list_id = card.list_id

    # اصلاح position کارت‌های لیست قدیمی
    old_list_cards = db.query(Card).filter(Card.list_id == old_list_id).order_by(Card.position).all()
    for c in old_list_cards:
        if c.position > card.position:
            c.position -= 1

    # افزایش position کارت‌های لیست جدید
    new_list_cards = db.query(Card).filter(Card.list_id == new_list_id).order_by(Card.position).all()
    for c in new_list_cards:
        if c.position >= new_position:
            c.position += 1

    card.list_id = new_list_id
    card.position = new_position
    db.commit()
    db.refresh(card)
    return card

# -----------------------
# جابجایی کارت با list_id (برای فرانت قدیمی)
# -----------------------
@router.patch("/lists/{list_id}/cards/{card_id}/move", response_model=CardResponse)
def move_card_with_list(list_id: int, card_id: int, new_list_id: int, new_position: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # اصلاح position کارت‌های لیست قدیمی
    old_list_cards = db.query(Card).filter(Card.list_id == list_id).order_by(Card.position).all()
    for c in old_list_cards:
        if c.position > card.position:
            c.position -= 1

    # افزایش position کارت‌های لیست جدید
    new_list_cards = db.query(Card).filter(Card.list_id == new_list_id).order_by(Card.position).all()
    for c in new_list_cards:
        if c.position >= new_position:
            c.position += 1

    card.list_id = new_list_id
    card.position = new_position
    db.commit()
    db.refresh(card)
    return card