# schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional


#create schema to validate the api inputs -> crud -> end points

class UserBase(BaseModel):
    """Shared properties for all user schemas"""
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str  # Include password for user creation

class UserUpdate(BaseModel):
    """Schema for updating an existing user"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    """Schema for user data stored in the database"""
    id: int
    hashed_password: str

    class Config:
        orm_mode = True
