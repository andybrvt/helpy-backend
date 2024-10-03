from pydantic import BaseModel
from typing import Optional, List
from schemas.alexadevice import AlexaDeviceResponse  # Import the correct AlexaDevice schema


# Schema for creating a new room
class RoomCreate(BaseModel):
    room_number: str
    resident_id: Optional[int] = None
    floor_number: Optional[int] = None
    room_type: Optional[str] = None

    class Config:
        orm_mode = True

# Schema for updating an existing room
class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    resident_id: Optional[int] = None
    floor_number: Optional[int] = None
    room_type: Optional[str] = None

    class Config:
        orm_mode = True

# Schema for returning room data in responses
class RoomResponse(BaseModel):
    id: int
    room_number: str
    community_id: int
    resident_id: Optional[int] = None
    floor_number: Optional[int] = None
    room_type: Optional[str] = None
    alexa_devices: List[AlexaDeviceResponse] = []  # Change to a list of AlexaDeviceResponse objects

    class Config:
        orm_mode = True
        from_attributes = True  # Add this line to allow ORM mapping
