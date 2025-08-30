from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base, SessionLocal
from app.routers.users import router as users_router
from app.models.user import User, UserRole
from app.utils.hashing import hash_password
from dotenv import load_dotenv
from app.routers import list_router
import os

load_dotenv()

Base.metadata.create_all(bind=engine)


KAVENEGAR_API_KEY = os.getenv("KAVENEGAR_API_KEY")

app = FastAPI()

app.include_router(users_router)
app.include_router(list_router.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Task Manager Backend is Running ✅"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        print("✅ Superadmin created -> Email: admin@example.com | Password: admin1234")
    else:
        print("ℹ️ Superadmin already exists.")

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        init_superadmin(db)
    finally:
        db.close()

