from pydantic import BaseModel, EmailStr,Field 
from typing import Optional
from datetime import datetime

# Schema for creating a community
class CommunityCreate(BaseModel):
    name: str
    address: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r'^\+?\d{10,15}$')  # Use 'pattern' instead of 'regex'


# Schema for updating a community
class CommunityUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r'^\+?\d{10,15}$')  # Use 'pattern' instead of 'regex'

# Schema for returning community data
class CommunityResponse(BaseModel):
    id: int
    name: str
    address: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    created_at: datetime
    created_by_id: int  # Include creator ID

    class Config:
        orm_mode = True  # This will allow reading from ORM models
