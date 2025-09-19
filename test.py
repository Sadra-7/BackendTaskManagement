from app.db.database import SessionLocal
from app.models.user import User
from app.models.task import Task

db = SessionLocal()

# 1. ایجاد یوزر تستی
new_user = User(username="testuser", hashed_password="1234")
db.add(new_user)
db.commit()
db.refresh(new_user)

print("User created:", new_user.id, new_user.username)

# 2. ایجاد تسک برای همون یوزر
task1 = Task(title="First task", user_id=new_user.id)
db.add(task1)
db.commit()
db.refresh(task1)

print("Task created:", task1.id, task1.title)

# 3. واکشی تسک‌ها از سمت یوزر
user_from_db = db.query(User).filter(User.id == new_user.id).first()
print("User tasks:", [t.title for t in user_from_db.tasks])