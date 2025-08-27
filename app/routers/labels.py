from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import label as label_schema
from app.crud import label_crud
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/labels", tags=["Labels"])

@router.post("/", response_model=label_schema.LabelOut)
def create_label(
    label: label_schema.LabelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return label_crud.create_label(db, label, current_user.id)

@router.get("/", response_model=List[label_schema.LabelOut])
def get_labels(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return label_crud.get_user_labels(db, current_user.id)