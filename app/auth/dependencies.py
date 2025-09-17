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
    
    
    token = credentials.credentials
    payload = verify_access_token(token)

    
    

    identity = payload.get("sub")

    
    if identity is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = db.query(User).filter(
        (User.email == identity) | (User.number == identity)
    ).first()
    

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