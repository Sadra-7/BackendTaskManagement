from sqlalchemy.orm import Session
from app.models.label import Label
from app.schemas.label import LabelCreate

def create_label(db: Session, label: LabelCreate, user_id: int):
    db_label = Label(**label.dict(), owner_id=user_id)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

def get_user_labels(db: Session, user_id: int):
    return db.query(Label).filter(Label.owner_id == user_id).all()