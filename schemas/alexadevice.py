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

# Room schema for response
class RoomResponse(BaseModel):
    id: int
    room_number: str
    floor_number: Optional[int] = None
    room_type: Optional[str] = None

    class Config:
        orm_mode = True

# Community schema for response
class CommunityResponse(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True

# Schema for Response
class AlexaDeviceResponse(AlexaDeviceBase):
    id: int
    room_id: int  # Include room_id directly
    community_id: Optional[int] = None  # Include community_id directly


    class Config:
        orm_mode = True
        from_attributes = True  # Add this line to allow ORM mapping

