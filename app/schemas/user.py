from pydantic import BaseModel, EmailStr , validator 
from typing import Optional
from enum import Enum
import re
# نقش‌های کاربران
class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"

# ====================
# اسکیمای پایه
# ====================
class UserBase(BaseModel):
    email_or_phone: str
    role: UserRole = UserRole.USER

    @validator("email_or_phone")
    def validate_email_or_phone(cls, v):
        
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        phone_regex = r"^\+?\d{10,15}$"

        if not (re.match(email_regex, v) or re.match(phone_regex, v)):
            raise ValueError("باید یک ایمیل معتبر یا شماره موبایل معتبر وارد کنید")
        return v
# ====================
# اسکیمای ساخت کاربر
# ====================
from pydantic import BaseModel, model_validator

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    number: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_email_or_number(self):
        if not self.email and not self.number:
            raise ValueError("حداقل یکی از ایمیل یا شماره باید وارد شود")
        return self

# ====================
# اسکیمای لاگین
# ====================
class UserLogin(BaseModel):
    email: Optional[str] = None
    number: Optional[str] = None
    password: str

    @model_validator(mode="before")
    def check_email_or_number(cls, values):
        if not values.get('email') and not values.get('number'):
            raise ValueError("Either email or number must be provided")
        return values
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
    username: str
    email: Optional[str] = None
    number: Optional[str] = None
    role: UserRole
    hashed_password: str   # 👈 پسورد هش شده (برای امنیت، متن خام نه)

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
    email: Optional[str] = None
    number: Optional[str] = None

    @model_validator(mode="before")
    def check_email_or_number(cls, values):
        if not values.get("email") and not values.get("number"):
            raise ValueError("Either email or number must be provided")
        return values

# ====================
# اسکیمای ریست رمز عبور
# ====================
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str