from passlib.context import CryptContext

# پیکربندی پسورد هشینگ
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# هش کردن رمز عبور
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# بررسی رمز عبور با هش ذخیره‌شده
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)