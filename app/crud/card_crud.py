from sqlalchemy.orm import Session
from app.models.card import Card

def create_card(db: Session, card, list_id: int):
    # position آخرین کارت + 1
    last_card = db.query(Card).filter(Card.list_id == list_id).order_by(Card.position.desc()).first()
    position = last_card.position + 1 if last_card else 0
    db_card = Card(text=card.text, list_id=list_id, position=position)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_cards_by_list(db: Session, list_id: int):
    return db.query(Card).filter(Card.list_id == list_id).order_by(Card.position).all()

def update_card(db: Session, card_id: int, new_text: str):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        card.text = new_text
        db.commit()
        db.refresh(card)
    return card

def delete_card(db: Session, card_id: int):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        db.delete(card)
        db.commit()
    return card

# ----------------------------
# تابع Drag & Drop اصلاح شده
# ----------------------------
def move_card(db: Session, card_id: int, new_list_id: int, new_position: int):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        return None

    old_list_id = card.list_id
    old_position = card.position

    if old_list_id == new_list_id:
        # جابجایی داخل همان لیست
        cards_in_list = db.query(Card).filter(Card.list_id == old_list_id).order_by(Card.position).all()
        cards_in_list.pop(old_position)
        cards_in_list.insert(new_position, card)
        # بروزرسانی پوزیشن همه کارت‌ها
        for idx, c in enumerate(cards_in_list):
            c.position = idx
    else:
        # جابجایی بین لیست‌ها
        # 1. لیست مبدا: کاهش پوزیشن کارت‌های بعد از کارت حذف شده
        cards_in_old = db.query(Card).filter(Card.list_id == old_list_id).order_by(Card.position).all()
        cards_in_old.pop(old_position)
        for idx, c in enumerate(cards_in_old):
            c.position = idx

        # 2. لیست مقصد: افزایش پوزیشن کارت‌ها بعد از new_position
        cards_in_new = db.query(Card).filter(Card.list_id == new_list_id).order_by(Card.position).all()
        cards_in_new.insert(new_position, card)
        for idx, c in enumerate(cards_in_new):
            c.position = idx

        card.list_id = new_list_id

    db.commit()
    db.refresh(card)
    return card