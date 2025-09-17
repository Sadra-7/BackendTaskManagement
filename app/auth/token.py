from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET_KEY = "your-very-secret-key"  # حتماً یک کلید طولانی و امن بذار
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

def create_access_token(data: dict, expires_delta: timedelta = None):

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str):

    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        return payload
    except JWTError as e:
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توکن نامعتبر یا منقضی شده است"
        )