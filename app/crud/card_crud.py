from sqlalchemy.orm import Session
from app import models, schemas

def create_card(db: Session, card: schemas.card.CardCreate, list_id: int):
    db_card = models.card.Card(text=card.text, list_id=list_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_cards_by_list(db: Session, list_id: int):
    return db.query(models.card.Card).filter(models.card.Card.list_id == list_id).all()

def update_card(db: Session, card_id: int, new_text: str):
    card = db.query(models.card.Card).filter(models.card.Card.id == card_id).first()
    if card:
        card.text = new_text
        db.commit()
        db.refresh(card)
    return card

def delete_card(db: Session, card_id: int):
    card = db.query(models.card.Card).filter(models.card.Card.id == card_id).first()
    if card:
        db.delete(card)
        db.commit()
    return card