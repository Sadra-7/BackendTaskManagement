from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.models.user import User, UserRole
from app.utils.hashing import verify_password
from app.auth.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.dependencies import get_current_user, require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


# ------------------------
# ورود ادمین
# ------------------------
@router.post("/login")
def admin_login(credentials: dict = Body(...), db: Session = Depends(get_db)):
    email = credentials.get("email")
    password = credentials.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="ایمیل و رمز عبور لازم است")

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="ایمیل یا رمز عبور اشتباه است")

    if user.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
        raise HTTPException(status_code=403, detail="شما دسترسی ادمین ندارید")

    token = create_access_token(
        data={"sub": user.email, "role": user.role.value},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"token": token, "role": user.role.value}


# ------------------------
# داشبورد ادمین
# ------------------------
@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SUPERADMIN]))
):
    return {"message": f"خوش آمدید {current_user.username} به داشبورد ادمین 🎉"}