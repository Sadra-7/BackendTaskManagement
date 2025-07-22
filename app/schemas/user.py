
from pydantic import BaseModel, EmailStr
# اسکیمای پایه برای پاسخ‌دهی (خواندن اطلاعات کاربر)
# User --> UserResponse
class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

# اسکیمای استفاده‌شده برای ایجاد کاربر جدید (نوشتن اطلاعات)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # یا orm_mode = True برای Pydantic v1