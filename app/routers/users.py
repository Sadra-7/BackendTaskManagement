from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User as UserModel, UserRole
from app.schemas.user import UserCreate, UserLogin, Token, UserOut, ForgotPasswordRequest, ResetPasswordRequest
from app.crud import user_crud
from app.auth.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.dependencies import get_current_user, require_role
from app.utils.hashing import hash_password, verify_password
from app.utils.send_email import send_email

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    send_email(
        to_email=user.email,
        subject="خوش آمدید!",
        body=f"{user.username} عزیز، ثبت‌نام شما با موفقیت انجام شد ✅"
    )
    return {"message": "User created successfully", "user_id": db_user.id}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role.value  # ✅ نقش کاربر در توکن
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user=Depends(get_current_user)):
    return {"user": current_user}

@router.get("/all", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, request.email)
    if not user:
        return {"message": "لینک بازیابی به ایمیل ارسال شد"}

    user = user_crud.set_reset_password_token(db, user)
    reset_link = f"http://localhost:3000/reset-password?token={user.reset_password_token}"
    send_email(
        to_email=user.email,
        subject="بازیابی رمز عبور",
        body=f"برای تغییر رمز خود روی این لینک کلیک کنید: {reset_link}"
    )
    return {"message": "لینک بازیابی به ایمیل ارسال شد"}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_reset_token(db, request.token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="توکن نامعتبر یا منقضی شده است")

    hashed_password = hash_password(request.new_password)
    user.hashed_password = hashed_password
    user.reset_password_token = None
    user.reset_password_expire = None

    db.add(user)
    db.commit()
    return {"message": "رمز عبور با موفقیت تغییر کرد"}

@router.patch(
    "/change-role/{user_id}",
    dependencies=[Depends(require_role([UserRole.SUPERADMIN]))]
)
def change_user_role(user_id: int, new_role: UserRole, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    user.role = new_role
    db.commit()
    db.refresh(user)
    return user