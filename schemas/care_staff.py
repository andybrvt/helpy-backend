# schemas/care_staff.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Schema for creating a new care staff member
class CareStaffCreate(BaseModel):
    name: str
    email: EmailStr
    role: str = "care_staff"  # Default role set to care staff
    password: str

# Schema for updating an existing care staff member
class CareStaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# Schema for reading care staff information
class CareStaffResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
