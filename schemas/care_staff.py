from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CareStaffCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100, description="Password must be between 8 and 100 characters.")
    community_id: Optional[int] = None  # Add community ID for association

class CareStaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)  # Apply same password validation


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
        orm_mode = True

class CareStaffResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    community: Optional[CommunityResponse]  # Include community details


    class Config:
        orm_mode = True
