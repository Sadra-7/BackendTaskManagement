from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token, UserOut
from app.crud import user_crud
from app.utils.token import create_access_token , SECRET_KEY, ALGORITHM
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()

# --------------------- ثبت نام ---------------------
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    return {"message": "User created successfully", "user_id": db_user.id}

# --------------------- ورود ---------------------
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user.email)
    if not db_user or not user_crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=1)  # ⏱ تغییر زمان انقضا از اینجا
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --------------------- اطلاعات یوزر فعلی ---------------------
@router.get("/me")
def read_users_me(current_user=Depends(get_current_user)):
    return {"user": current_user}

# --------------------- گرفتن لیست کل کاربران ---------------------
@router.get("/all", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users