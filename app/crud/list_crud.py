from sqlalchemy.orm import Session
from app.models.list import List
from app.models.card import Card
from app.schemas import list as list_schema

def get_lists(db: Session , user_id : int):
    return db.query(List).filter(List.user_id == user_id ).all()

def create_list(db: Session, list_in: list_schema.ListCreate , user_id : int):
    db_list = List(**list_in.dict(), user_id=user_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def delete_list(db: Session, list_id: int):
    db_list = db.query(List).filter(List.id == list_id).first()  
    if db_list:
        db.delete(db_list)
        db.commit()
    return db_list

def add_card(db: Session, list_id: int, card_in):
    db_card = Card(list_id=list_id, text=card_in.text)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, list_id: int, card_id: int):
    db_card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if db_card:
        db.delete(db_card)
        db.commit()
    return db_card

def update_list(db: Session, list_id: int, user_id: int, title: str = None, color: str = None):
    db_list = db.query(List).filter_by(id=list_id, user_id=user_id).first()
    if not db_list:
        return None
    if title:
        db_list.title = title
    if color:
        db_list.color = color
    db.commit()
    db.refresh(db_list)
    return db_list

def update_card(db: Session, list_id: int, card_id: int, text: str):
    db_card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if not db_card:
        return None
    db_card.text = text
    db.commit()
    db.refresh(db_card)
    return db_card