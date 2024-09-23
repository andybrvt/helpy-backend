# routers/user.py
from fastapi import APIRouter, Depends, HTTPException, Security, Form
from sqlalchemy.ext.asyncio import AsyncSession  # Use AsyncSession instead of Session
from typing import List
from datetime import timedelta

from database_configs.db import get_db  # Ensure this returns AsyncSession
from schemas.user import UserCreate, UserUpdate, UserInDB, UserResponse, UserLogin, OAuth2Login
from crud.crud_user import get_user, get_users, create_user, update_user, delete_user, get_user_by_email
from auth.jwt import create_access_token  # Assuming you have a JWT utility module
from config import ACCESS_TOKEN_EXPIRE_MINUTES  # JWT expiration setting
from auth.utils import get_password_hash, verify_password  # Import the bcrypt utility functions
from auth.dependencies import get_current_user  # Import the authentication dependency



#router = APIRouter(dependencies=[Depends(get_current_user)])
router = APIRouter()



# Asynchronous route handler for reading all users
@router.get("/users/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    users = await get_users(db, skip=skip, limit=limit)  # Await the async function
    return users

# Asynchronous route handler for reading a specific user by ID
@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    db_user = await get_user(db, user_id=user_id)  # Await the async function
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Asynchronous route handler for creating a new user
@router.post("/users/", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    db_user = await get_user_by_email(db, email=user.email)  # Await the async function
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password using the utility function from auth/utils.py
    user.password = get_password_hash(user.password)
    
    created_user = await create_user(db=db, user=user)  # Await the async function
    return UserResponse.from_orm(created_user)  # Return a UserResponse model

# Asynchronous route handler for updating an existing user
@router.put("/users/{user_id}", response_model=UserResponse)
async def update_existing_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    updated_user = await update_user(db=db, user_id=user_id, user_update=user)  # Await the async function
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(updated_user)  # Return a UserResponse model

# Asynchronous route handler for deleting an existing user
@router.delete("/users/{user_id}", response_model=UserResponse)
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    deleted_user = await delete_user(db=db, user_id=user_id)  # Await the async function
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(deleted_user)  # Return a UserResponse model

# Asynchronous registration route handler
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)  # Await the async function
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
     # Hash the password using the utility function from auth/utils.py
    plain_password = user.password  # Store the plain password for debugging
    hashed_password = get_password_hash(plain_password)
    
    # Debugging: Print the plain password and hashed password
    print(f"Plain Password: {plain_password}")  # This will print the user's entered plain password
    print(f"Hashed Password: {hashed_password}")  # This will print the hashed password

    # Update the user object with the hashed password
    user.password = hashed_password

    created_user = await create_user(db=db, user=user)  # Await the async function
    return UserResponse.from_orm(created_user)  # Return a UserResponse model

# Asynchronous login route handler
@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    print('does it hit?')
    db_user = await get_user_by_email(db, email=user.email)  # Await the async function
    if db_user:
        print(f"Entered Password: {user.password}")  # Debugging
        print(f"Stored Hashed Password: {db_user.hashed_password}")  # Debugging
    
    # Check if the user exists and the password is correct using the utility function
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        print("Password verification failed")  # Debugging
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Create a JWT token for the user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/oauth2-login")
async def oauth2_login(
    username: str = Form(...),  # Accept form data for username
    password: str = Form(...),  # Accept form data for password
    db: AsyncSession = Depends(get_db)
):
    db_user = await get_user_by_email(db, email=username)  # Use username as email
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


'''
{
    "name": "John Doe",                    
    "email": "johndoe12@example.com",        
    "role": "staff",                         
    "password": "StrongPass123!"            
}
'''