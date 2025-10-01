import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.db.database import engine, Base, SessionLocal
from app.routers.users import router as users_router
from app.routers import users, boards, cards, list_router, admin, workspaces
from app.routers.boards import router as boards_router
from app.routers.list_router import router as list_router
from app.routers import cards  # اضافه شد
from app.models.user import User, UserRole
from app.utils.hashing import hash_password
from app.auth.dependencies import get_current_user


# Load environment variables
load_dotenv()

# Create tables (در صورت استفاده از Alembic فقط برای dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager Backend")

# CORS middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://niktick.ir",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)            
app.include_router(boards_router)           
app.include_router(list_router)             
app.include_router(cards.router)            
app.include_router(admin.router)        
app.include_router(workspaces.router)   


# Root endpoint
@app.get("/")
def root():
    return {"message": "Task Manager Backend is Running ✅"}

# Debug token endpoint
@app.get("/debug-token")
def debug_token(current_user: User = Depends(get_current_user)):
    return {"user": current_user}

# Initialize superadmin on startup
def init_superadmin(db):
    superadmin_email = "sadra.amini1006@gmail.com"
    existing = db.query(User).filter(User.email == superadmin_email).first()

    if not existing:
        new_superadmin = User(
            username="superadmin",
            email=superadmin_email,
            hashed_password=hash_password("admin1234"),
            role=UserRole.SUPERADMIN
        )
        db.add(new_superadmin)
        db.commit()
        print(f"✅ Superadmin created -> Email: {superadmin_email} | Password: admin1234")
    else:
        print("ℹ️ Superadmin already exists.")

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        init_superadmin(db)
    finally:
        db.close()