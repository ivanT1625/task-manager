from sqlalchemy.orm import Session
from . import models
import uuid as uuid_lib


def get_task(db: Session, uuid: str):
    return db.query(models.TaskModel).filter(models.TaskModel.uuid == uuid).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TaskModel).offset(skip).limit(limit).all()

def create_task(db: Session, task:dict):
    uuid = str(uuid_lib.uuid4())
    db_task = models.TaskModel(
        uuid = uuid,
        title = task["title"],
        description = task.get("description"),
        status = task.get("status", "created")
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, uuid: str, task_data: dict):
    db_task = get_task(db,uuid)
    if not db_task:
        return None
    for key, value in task_data.items():
        if value is not None:
            setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, uuid: str):
    db_task = get_task(db, uuid)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True
    