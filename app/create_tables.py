from app.db.database import Base, engine
from app.models.user import User
from app.models.list import List
from app.models.card import Card
from app.models.task import Task

print("🛠️ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")