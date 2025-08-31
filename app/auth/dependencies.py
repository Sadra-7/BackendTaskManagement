from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User, UserRole
from .token import verify_access_token

security = HTTPBearer()

def get_current_user(
    
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    
    print("get current")
    token = credentials.credentials
    payload = verify_access_token(token)

    print("Payload:", payload)  # 🔹 اضافه شده برای دیباگ
    

    identity = payload.get("sub")

    print("Identity:", identity)
    if identity is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = db.query(User).filter(
        (User.email == identity) | (User.number == identity)
    ).first()
    print("User from DB: " , user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# -------------------------------
# Require role decorator / dependency
# -------------------------------
def require_role(allowed_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return current_user
    return role_checker