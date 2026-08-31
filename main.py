from fastapi import FastAPI
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends
from routers.tasks import router as task_router
from routers.auth import router as auth_router
from db import create_db_and_table

app = FastAPI()

@app.on_event("startup")
def on_starttup():
    create_db_and_table()

app.include_router(task_router)

@app.get('/home/name')
def get_something(name):
    return f"Hello {name}"

app.include_router(auth_router)