from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None  # Allow description to be None
    status: str
    priority_score: int
    created_at: datetime

    class Config:
        orm_mode = True
