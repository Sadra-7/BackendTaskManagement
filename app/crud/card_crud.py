from sqlalchemy.orm import Session
from app.models.card import Card
from app.schemas.card import CardCreate, CardUpdate

def get_card(db: Session, card_id: int):
    return db.query(Card).filter(Card.id == card_id).first()

def create_card(db: Session, card: CardCreate):
    db_card = Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def update_card(db: Session, card_id: int, card_update: CardUpdate):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        return None
    for key, value in card_update.dict(exclude_unset=True).items():
        setattr(card, key, value)
    db.commit()
    db.refresh(card)
    return card

def delete_card(db: Session, card_id: int):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        return None
    db.delete(card)
    db.commit()
    return card