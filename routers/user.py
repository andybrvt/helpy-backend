# routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  # Use AsyncSession instead of Session
from typing import List
from passlib.context import CryptContext  # For password hashing
from datetime import timedelta

from database_configs.db import get_db  # Ensure this returns AsyncSession
from schemas.user import UserCreate, UserUpdate, UserInDB, UserResponse
from crud.crud_user import get_user, get_users, create_user, update_user, delete_user, get_user_by_email
from auth.jwt import create_access_token  # Assuming you have a JWT utility module
from config import ACCESS_TOKEN_EXPIRE_MINUTES  # JWT expiration setting


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Asynchronous route handler for reading all users
@router.get("/users/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await get_users(db, skip=skip, limit=limit)  # Await the async function
    return users

# Asynchronous route handler for reading a specific user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id=user_id)  # Await the async function
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



# Asynchronous route handler for creating a new user
@router.post("/users/", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)  # Await the async function
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db=db, user=user)  # Await the async function


# Asynchronous route handler for updating an existing user
@router.put("/users/{user_id}", response_model=UserResponse)
async def update_existing_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await update_user(db=db, user_id=user_id, user_update=user)  # Await the async function
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Asynchronous route handler for deleting an existing user
@router.delete("/users/{user_id}", response_model=UserResponse)
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted_user = await delete_user(db=db, user_id=user_id)  # Await the async function
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user


# Asynchronous registration route handler
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)  # Await the async function
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = get_password_hash(user.password)  # Hash the password
    return await create_user(db=db, user=user)  # Await the async function


# Asynchronous login route handler
@router.post("/login")
async def login_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)  # Await the async function
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Create a JWT token for the user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}