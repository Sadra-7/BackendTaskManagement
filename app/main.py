
from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import users
from app.routers.users import router as users_router
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router)

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Task Manager Backend is Running ✅"}







# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

