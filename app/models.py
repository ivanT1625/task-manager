from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class TaskStatus(str, enum.Enum):
    created  = "created"
    in_progress = "in_progress"
    completed = "completed"

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.created)



