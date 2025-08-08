from pydantic import BaseModel, EmailStr
from enum import Enum

# نقش‌های کاربران
class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"

# ====================
# اسکیمای پایه
# ====================
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.USER  # مقدار پیش‌فرض برای نقش

# ====================
# اسکیمای ساخت کاربر
# ====================
class UserCreate(UserBase):
    username: str
    password: str

# ====================
# اسکیمای لاگین
# ====================
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ====================
# اسکیمای خروجی کاربر (برای نمایش در پاسخ‌ها)
# ====================
class UserResponse(UserBase):
    id: int
    username: str

    class Config:
        from_attributes = True  # یا from_attributes در Pydantic v2

# ====================
# اسکیمای خلاصه خروجی برای فرانت
# ====================
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole  # 👈 اضافه شده

    class Config:
        from_attributes = True

# ====================
# اسکیمای توکن JWT
# ====================
class Token(BaseModel):
    access_token: str
    token_type: str

# ====================
# اسکیمای فراموشی رمز
# ====================
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# ====================
# اسکیمای ریست رمز عبور
# ====================
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str