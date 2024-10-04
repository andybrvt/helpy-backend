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
    community_id: Optional[int] = None  # Add community ID (optional in case the task isn't associated with a community)
    room_id: Optional[int] = None  # Add room ID (optional in case the task isn't associated with a room)
    alexa_device_id: Optional[int] = None  # Add Alexa device ID (optional in case the task isn't associated with an Alexa device)

    class Config:
        orm_mode = True
