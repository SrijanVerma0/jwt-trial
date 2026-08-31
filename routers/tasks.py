from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from db import create_db_and_table,get_session,Task,TaskCreate

router = APIRouter(prefix="/task")

@router.post("/")
def post_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("")
def get_task(session: Session = Depends(get_session)):
    tasks = session.execute(select(Task)).scalars().all()
    return tasks

@router.put("/{task_id}")
def update_task(task_id: int, changed: Task, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        return {"error": "Task not found"}
    db_task.title = changed.title
    db_task.done = changed.done
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        return {"error": "Task not found"}
    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted"}