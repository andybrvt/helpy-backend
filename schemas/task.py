from pydantic import BaseModel
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority_score: int
    created_at: datetime

    class Config:
        orm_mode = True
