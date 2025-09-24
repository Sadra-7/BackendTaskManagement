# app/routers/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.models.user import User, UserRole
from app.models.board import Board
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
class CreateBoard(BaseModel):
    title: str

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
# دریافت همه کاربران به همراه بردها و لیست‌ها
# ------------------------
@router.get("/users-with-lists")
def get_users_with_boards(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role.value,
            "boards": [
                {
                    "id": b.id,
                    "title": b.title,
                    "lists": [
                        {
                            "id": l.id,
                            "title": l.title,
                            "cards": [{"id": c.id, "text": c.text} for c in l.cards]
                        }
                        for l in b.lists
                    ]
                }
                for b in u.boards
            ]
        }
        for u in users
    ]

# ------------------------
# دریافت همه بردها
# ------------------------
@router.get("/boards")
def get_all_boards(db: Session = Depends(get_db)):
    boards = db.query(Board).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "owner_id": b.owner_id,
            "lists": [
                {
                    "id": l.id,
                    "title": l.title,
                    "cards": [{"id": c.id, "text": c.text} for c in l.cards],
                }
                for l in b.lists
            ],
        }
        for b in boards
    ]

# ------------------------
# دریافت بردهای یک کاربر
# ------------------------
@router.get("/users/{user_id}/boards")
def get_user_boards(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    return [
        {
            "id": b.id,
            "title": b.title,
            "lists": [
                {
                    "id": l.id,
                    "title": l.title,
                    "cards": [{"id": c.id, "text": c.text} for c in l.cards]
                }
                for l in b.lists
            ]
        }
        for b in user.boards
    ]

# ------------------------
# ساخت برد جدید برای یک کاربر
# ------------------------
@router.post("/users/{user_id}/boards")
def create_board_admin(user_id: int, data: CreateBoard, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر یافت نشد")
    new_board = Board(title=data.title, owner_id=user_id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return {
        "message": "برد ساخته شد",
        "board": {"id": new_board.id, "title": new_board.title, "owner_id": new_board.owner_id}
    }

# ------------------------
# دریافت لیست‌های یک برد مشخص
# ------------------------
@router.get("/boards/{board_id}/lists")
def get_board_lists(board_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="برد یافت نشد")
    return [
        {
            "id": l.id,
            "title": l.title,
            "cards": [{"id": c.id, "text": c.text} for c in l.cards],
        }
        for l in board.lists
    ]

# ------------------------
# ساخت لیست جدید در یک برد
# ------------------------
@router.post("/boards/{board_id}/lists")
def create_list_admin(board_id: int, data: CreateList, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="برد یافت نشد")
    new_list = List(title=data.title, board_id=board_id, user_id=board.owner_id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return {"message": "لیست ساخته شد", "list": {"id": new_list.id, "title": new_list.title}}

# ------------------------
# ساخت کارت جدید در یک لیست
# ------------------------
@router.post("/lists/{list_id}/cards")
def create_card_admin(list_id: int, data: CreateCard, db: Session = Depends(get_db)):
    lst = db.query(List).filter(List.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="لیست یافت نشد")
    new_card = Card(text=data.text, list_id=list_id)
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return {"message": "کارت ساخته شد", "card": {"id": new_card.id, "text": new_card.text}}

# ------------------------
# تغییر نقش کاربر
# ------------------------
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