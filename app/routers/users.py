from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
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
from app.utils.send_massage import send_sms
from app.models.user import User

router = APIRouter()
security = HTTPBearer()

# =======================
# ثبت‌نام کاربر
# =======================
@router.post("/users/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(status_code=400, detail="نام کاربری قبلاً استفاده شده است")
    if user.email and db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=400, detail="ایمیل قبلاً استفاده شده است")
    if user.number and db.query(UserModel).filter(UserModel.number == user.number).first():
        raise HTTPException(status_code=400, detail="شماره تلفن قبلاً استفاده شده است")

    db_user = user_crud.create_user(db, user)

    if db_user.email:
        send_email(
            to_email=db_user.email,
            subject="خوش آمدید!",
            body=f"{db_user.username} عزیز، ثبت‌نام شما با موفقیت انجام شد ✅"
        )
    
    return {"message": "User created successfully", "user_id": db_user.id}


# =======================
# ورود کاربر و ایجاد توکن
# =======================
@router.post("/users/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    if user.email:
        db_user = user_crud.get_user_by_email(db, user.email)
    else:
        db_user = user_crud.get_user_by_number(db, user.number)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": db_user.email or db_user.number,
            "role": db_user.role.value
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# =======================
# اطلاعات کاربر فعلی
# =======================
@router.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {"user": current_user}

# =======================
# گرفتن همه کاربران (فقط برای سوپرادمین)
# =======================
@router.get("/users/all", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db), current_user=Depends(require_role([UserRole.SUPERADMIN]))):
    users = db.query(UserModel).all()
    return users


# =======================
# فراموشی رمز عبور
# =======================
@router.post("/users/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = None
    if request.email:
        user = user_crud.get_user_by_email(db, request.email)
    elif request.number:
        user = user_crud.get_user_by_number(db, request.number)

    if not user:
        return {"message": "لینک یا کد بازیابی ارسال شد"}

    user = user_crud.set_reset_password_token(db, user)
    reset_link = f"http://localhost:3000/reset-password?token={user.reset_password_token}"

    if request.email:
        send_email(
            to_email=user.email,
            subject="بازیابی رمز عبور",
            body=f"برای تغییر رمز خود روی این لینک کلیک کنید: {reset_link}"
        )
    else:
        send_sms(
            user.number,
            message=f"برای تغییر رمز خود روی این لینک کلیک کنید: {reset_link}"
        )

    return {"message": "لینک یا کد بازیابی ارسال شد"}


# =======================
# ریست رمز عبور
# =======================
@router.post("/users/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_reset_token(db, request.token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="توکن نامعتبر یا منقضی شده است")

    hashed_password = hash_password(request.new_password)
    user.hashed_password = hashed_password
    user.reset_password_token = None
    user.reset_password_expire = None

    db.commit()
    db.refresh(user)
    return {"message": "رمز عبور با موفقیت تغییر کرد ✅"}


# =======================
# تغییر نقش کاربر (فقط برای سوپرادمین)
# =======================
@router.patch("/users/change-role/{user_id}", dependencies=[Depends(require_role([UserRole.SUPERADMIN]))])
def change_user_role(user_id: int, new_role: UserRole, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    user.role = new_role
    db.commit()
    db.refresh(user)
    return user

