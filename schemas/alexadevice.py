from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base Schema
class AlexaDeviceBase(BaseModel):
    device_id: str
    room_id: int
    community_id: Optional[int] = None
    status: Optional[str] = "active"
    last_synced: Optional[datetime] = None
    last_request: Optional[datetime] = None
    total_number_requested: Optional[int] = 0

# Schema for Creating a Device
class AlexaDeviceCreate(AlexaDeviceBase):
    pass

# Schema for Updating a Device
class AlexaDeviceUpdate(BaseModel):
    status: Optional[str] = None
    last_synced: Optional[datetime] = None
    last_request: Optional[datetime] = None
    total_number_requested: Optional[int] = None

# Schema for Response
class AlexaDeviceResponse(AlexaDeviceBase):
    id: int

    class Config:
        orm_mode = True
