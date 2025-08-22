
from typing import Optional
from pydantic import BaseModel
import uuid

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]=None
    status: Optional[str]="created"

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Fix login bug",
                "description": "User cannot log in after password reset.",
                "status": "created"
            }
        }
      }

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    uuid: str
    title: str
    description: Optional[str] = None
    status: str

    model_config = {"from_attributes": True}