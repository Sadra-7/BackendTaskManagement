from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin, Token
from app.crud import user_crud as user_crud
from app.auth import create_access_token
from app import models , schemas , auth , crud
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from app.auth import get_current_user



from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    return {"message": "User created successfully", "user_id": db_user.id}



# @router.post("/login", response_model=Token)
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user_by_email(db, user.email)
#     if not db_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#     if not user_crud.verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

#     access_token = create_access_token(data={"sub": db_user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user.email)
    if not db_user or not user_crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # ✅ اضافه شدن مدت اعتبار توکن
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=1)
    )
    return {"access_token": access_token, "token_type": "bearer"}


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.crud import user_crud
from app.schemas.user import User
from app.auth import SECRET_KEY, ALGORITHM

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# @router.get("/me", response_model=User)
# def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         user = user_crud.get_user_by_email(db, email)
#         if user is None:
#             raise HTTPException(status_code=401, detail="User not found")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token expired or invalid")


# sljdfhgiuwhgiouaqhrgui

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     # decode token ...

@router.get("/me")
def read_users_me(current_user=Depends(get_current_user)):
    return {"user": current_user}
    


from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.db.database import get_db  # تابع گرفتن سشن DB
from app.models.user import User  # مدل SQLAlchemy دیتابیس
from app.schemas.user import User  # مدل Pydantic

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User  # SQLAlchemy مدل
from app.schemas.user import UserOut  # Pydantic مدل

# router = APIRouter()

@router.get("/users/all", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users