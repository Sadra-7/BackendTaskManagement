from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password
from passlib.context import CryptContext
from datetime import datetime
from app.db.database import SessionLocal

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def set_reset_password_token(db, user: User):
    user.generate_reset_token()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_reset_token(db, token: str):
    return db.query(User).filter(
        User.reset_password_token == token,
        User.reset_password_expire > datetime.utcnow()
    ).first()
