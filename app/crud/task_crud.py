# app/crud/task_crud.py
from sqlalchemy.orm import Session
from app.models.task import Task

def create_task(db: Session, title: str, user_id: int, description: str = None):
    task = Task(title=title, description=description, assigned_to=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_for_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.assigned_to == user_id).all()