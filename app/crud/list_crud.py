from sqlalchemy.orm import Session
from app.models.list import List
from app.models.card import Card
from app.schemas import list as list_schema

# Lists
def get_lists(db: Session, board_id: int):
    return db.query(List).filter(List.board_id == board_id).all()

def create_list(db: Session, board_id: int, list_in: list_schema.ListCreate):
    db_list = List(title=list_in.title, color=list_in.color or "#ffffff", board_id=board_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def update_list(db: Session, list_id: int, title: str = None, color: str = None):
    db_list = db.query(List).filter(List.id == list_id).first()
    if not db_list:
        return None
    if title is not None:
        db_list.title = title
    if color is not None:
        db_list.color = color
    db.commit()
    db.refresh(db_list)
    return db_list

def delete_list(db: Session, list_id: int):
    db_list = db.query(List).filter(List.id == list_id).first()
    if db_list:
        db.delete(db_list)
        db.commit()
    return db_list

# Cards
def add_card(db: Session, list_id: int, card_in: list_schema.CardCreate):
    last_position = db.query(Card).filter(Card.list_id == list_id).count()
    db_card = Card(list_id=list_id, text=card_in.text, position=last_position)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def update_card(db: Session, list_id: int, card_id: int, text: str = None, new_list_id: int = None, position: int = None):
    db_card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if not db_card:
        return None
    if text is not None:
        db_card.text = text
    if new_list_id is not None:
        db_card.list_id = new_list_id
    if position is not None:
        db_card.position = position
    db.commit()
    db.refresh(db_card)
    return db_card

def delete_card(db: Session, list_id: int, card_id: int):
    db_card = db.query(Card).filter(Card.id == card_id, Card.list_id == list_id).first()
    if db_card:
        db.delete(db_card)
        db.commit()
    return db_card