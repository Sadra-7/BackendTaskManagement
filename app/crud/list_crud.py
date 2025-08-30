from sqlalchemy.orm import Session
from app.models.list import List
from app.models.card import Card
from app.schemas import list as list_schema

def get_lists(db: Session):

    return db.query(List).all()

def create_list(db: Session, list_in: list_schema.ListCreate):
    db_list = List(**list_in.dict())
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

def add_card(db: Session, list_id: int, card_in: list_schema.CardCreate):
    db_card = Card(list_id=list_id, **card_in.dict())
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