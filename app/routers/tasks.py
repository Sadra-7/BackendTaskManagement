from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.models.task import Task
from app.schemas import task as task_schema
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.crud import task_crud
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])



@router.post("/", response_model=task_schema.TaskOut)
def create_task(
    task: task_schema.TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_crud.create_task(db, task, current_user.id)

@router.get("/", response_model=List[task_schema.TaskOut])
def get_user_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_crud.get_user_tasks(db, current_user.id)

@router.put("/{task_id}", response_model=task_schema.TaskOut)
def update_task(
    task_id: int,
    task_data: task_schema.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = task_crud.update_task(db, task_id, task_data)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = task_crud.delete_task(db, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Deleted"}

# روت اصلاح‌شده برای ذخیره چند تسک به صورت همزمان
@router.post("/save", response_model=dict)
def save_tasks(
    task_list: task_schema.TaskList,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # حذف تسک‌های قبلی فقط برای کاربر جاری
    db.query(Task).filter(Task.owner_id == current_user.id).delete()
    db.commit()

    saved = []
    for task in task_list.tasks:
        saved_task = task_crud.create_task(db, task, current_user.id)
        saved.append(saved_task)

    return {"status": "success", "saved": len(saved)}
