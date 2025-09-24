from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List as TypingList
from app.db.database import get_db
from app.models.card import Card
from app.models.list import List as ListModel
from app.schemas.card import CardCreate, CardUpdate, CardResponse

router = APIRouter(
    prefix="/lists/{list_id}/cards",
    tags=["Cards"]
)

# Get all cards of a list
@router.get("/", response_model=TypingList[CardResponse])
def get_cards(list_id: int, db: Session = Depends(get_db)):
    list_obj = db.query(ListModel).filter(ListModel.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    return list_obj.cards

# Create a new card
@router.post("/", response_model=CardResponse)
def create_card(list_id: int, card_in: CardCreate, db: Session = Depends(get_db)):
    list_obj = db.query(ListModel).filter(ListModel.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    
    # تعیین position آخرین کارت
    last_position = db.query(Card).filter(Card.list_id == list_id).order_by(Card.position.desc()).first()
    position = last_position.position + 1 if last_position else 0

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

# Update a card
@router.put("/{card_id}", response_model=CardResponse)
def update_card(list_id: int, card_id: int, card_in: CardUpdate, db: Session = Depends(get_db)):
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

# Delete a card
@router.delete("/{card_id}")
def delete_card(list_id: int, card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return {"detail": "Card deleted"}

# Move card to another list or position
@router.patch("/{card_id}/move", response_model=CardResponse)
def move_card(
    list_id: int,
    card_id: int,
    new_list_id: int,
    new_position: int,
    db: Session = Depends(get_db)
):
    card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # حذف از لیست قدیمی
    old_list_cards = db.query(Card).filter(Card.list_id == list_id).order_by(Card.position).all()
    for c in old_list_cards:
        if c.position > card.position:
            c.position -= 1

    # افزودن به لیست جدید
    new_list_cards = db.query(Card).filter(Card.list_id == new_list_id).order_by(Card.position).all()
    for c in new_list_cards:
        if c.position >= new_position:
            c.position += 1

    card.list_id = new_list_id
    card.position = new_position
    db.commit()
    db.refresh(card)
    return card