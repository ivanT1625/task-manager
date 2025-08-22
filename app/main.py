from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from . import models, schemas, crud, database


app = FastAPI(
    title = "Task Manager API",
    description = "CRUD API для управления задачами",
    version = "1.0.0"
)

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager API. Visit /docs for Swagger."}

@app.post("/tasks/", response_model = schemas.TaskResponse, status_code =status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db, task.dict())

@app.get("/tasks/{uuid}", response_model = schemas.TaskResponse)
def read_task(uuid: str, db: Session = Depends(database.get_db)):
    db_task = crud.get_task(db, uuid)
    if not db_task:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return db_task

@app.get("/tasks/", response_model = List[schemas.TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10 , db: Session  = Depends(database.get_db)):
    tasks = crud.get_tasks(db,skip=skip,limit=limit)
    return tasks

@app.put("/tasks/{uuid}", response_model = schemas.TaskResponse)
def update_task(uuid: str, task : schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    updated_task = crud.update_task(db, uuid, task.dict(exclude_unset=True))
    if not updated_task:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return updated_task

@app.delete("/tasks/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(uuid: str, db: Session = Depends(database.get_db)):
    success = crud.delete_task(db, uuid)
    if not success:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return

