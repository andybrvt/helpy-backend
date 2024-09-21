# schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re  # Add this line to import the 're' module


#create schema to validate the api inputs -> crud -> end points
# List of common passwords to avoid
common_passwords = ["password", "12345678", "qwerty", "letmein", "welcome"]



class UserBase(BaseModel):
    """Shared properties for all user schemas"""
    name: str = Field(..., min_length=2, max_length=50, description="User's name must be between 2 and 50 characters")
    email: EmailStr
    role: str = Field(..., description="User role, e.g., 'admin' or 'user'")

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=100, 
        description="Password must be between 8 and 100 characters, and contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    )

    @validator('password')
    def validate_password(cls, value):
        # Regular expression for password validation
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', value):
            raise ValueError(
                'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'
            )
        if value.lower() in common_passwords:
            raise ValueError('Password is too common. Please choose a stronger password.')
        return value


class UserUpdate(BaseModel):
    """Schema for updating an existing user"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    """Schema for user data stored in the database"""
    id: int
    hashed_password: str  # Use 'password' to match database field

    class Config:
        orm_mode = True

# Define a separate model for response without password
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
        from_attributes = True

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str



