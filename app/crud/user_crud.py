from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        number=user.number,
        hashed_password=hash_password(user.password),
        role="USER"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_number(db: Session, number: str) -> User | None:
    return db.query(User).filter(User.number == number).first()

def get_user_by_email_or_number(db: Session, identifier: str) -> User | None:
    user = get_user_by_email(db, identifier)
    if not user:
        user = get_user_by_number(db, identifier)
    return user

def set_reset_password_token(db: Session, user: User, expire_hours: int = 1) -> User:
    token = secrets.token_urlsafe(32)
    user.reset_password_token = token
    user.reset_password_expire = datetime.utcnow() + timedelta(hours=expire_hours)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_reset_token(db: Session, token: str) -> User | None:
    user = db.query(User).filter(User.reset_password_token == token).first()
    if not user or not user.reset_password_expire or user.reset_password_expire < datetime.utcnow():
        return None
    return user