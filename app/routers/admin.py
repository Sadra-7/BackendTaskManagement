# app/routers/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.models.user import User, UserRole
from app.models.list import List
from app.models.card import Card
from app.utils.hashing import verify_password
from app.auth.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.user import Token, AdminLogin
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])


# ------------------------
# Pydantic Models
# ------------------------
class CreateList(BaseModel):
    title: str


class CreateCard(BaseModel):
    text: str


class ChangeUserRole(BaseModel):
    new_role: str


# ------------------------
# ورود ادمین
# ------------------------
@router.post("/login", response_model=Token)
def admin_login(data: AdminLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == data.email).first()

    if not db_user or not verify_password(data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور اشتباه است"
        )

    if db_user.role not in [UserRole.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="شما دسترسی ادمین ندارید"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "user_id": db_user.id,
            "role": db_user.role.value
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ------------------------
# داشبورد ادمین
# ------------------------

# 1️⃣ دریافت همه کاربران همراه با لیست‌ها و کارت‌ها
@router.get("/users-with-lists")
def get_users_with_lists(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role.value,
            "lists": [
                {
                    "id": l.id,
                    "title": l.title,
                    "cards": [{"id": c.id, "text": c.text} for c in l.cards],
                }
                for l in u.lists
            ],
        }
        for u in users
    ]


# 2️⃣ ساخت لیست جدید برای یک کاربر
@router.post("/users/{user_id}/lists")
def create_list(user_id: int, data: CreateList, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    new_list = List(title=data.title, user_id=user_id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return {"message": "لیست ساخته شد", "list": {"id": new_list.id, "title": new_list.title}}


# 3️⃣ ساخت کارت جدید داخل لیست
@router.post("/lists/{list_id}/cards")
def create_card(list_id: int, data: CreateCard, db: Session = Depends(get_db)):
    lst = db.query(List).filter(List.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="لیست یافت نشد")
    new_card = Card(text=data.text, list_id=list_id)
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return {"message": "کارت ساخته شد", "card": {"id": new_card.id, "text": new_card.text}}


# 4️⃣ تغییر نقش کاربر
@router.patch("/change-role/{user_id}")
def change_role(user_id: int, data: ChangeUserRole, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")

    try:
        new_role = UserRole(data.new_role)
    except ValueError:
        raise HTTPException(status_code=400, detail="نقش نامعتبر است")

    user.role = new_role
    db.commit()
    return {"message": f"نقش کاربر {user.username} تغییر کرد به {new_role.value}"}