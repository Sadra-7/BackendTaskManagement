from app.db.database import engine
from app.models.user import User
from app.db.database import Base

print("🛠️ Creating tables...")

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully.")