import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import boards


from app.db.database import engine, Base, SessionLocal
from app.routers.users import router as users_router
from app.routers import list_router, admin
from app.models.user import User, UserRole
from app.utils.hashing import hash_password
from app.auth.dependencies import get_current_user

# Load .env
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

KAVENEGAR_API_KEY = os.getenv("KAVENEGAR_API_KEY")

app = FastAPI()

# Include routers
app.include_router(users_router)
app.include_router(list_router.router, prefix="/api")
app.include_router(admin.router)
app.include_router(boards.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Task Manager Backend is Running ✅"}

# Debug token
@app.get("/debug-token")
def debug_token(current_user: User = Depends(get_current_user)):
    return {"user": current_user}

# CORS middleware
origins = [
    "http://localhost:3000",  # برای لوکال
    "http://127.0.0.1:3000",
    "http://niktick.ir",      # برای سرور
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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