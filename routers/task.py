from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database_configs.db import get_db  # Ensure this is the correct path to your DB config
from models.models import Task  # Import the Task model
from schemas.task import TaskResponse  # Import or create Task schema for response
from auth.dependencies import get_current_user  # Import the authentication dependency
from schemas.user import UserInDB  # Import the authenticated user model
from sqlalchemy.future import select  # Import the select function for querying

router = APIRouter()

@router.get("/tasks/", response_model=List[TaskResponse])
async def get_all_tasks(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)  # Authentication dependency
):
    # Query all tasks with pagination
    result = await db.execute(select(Task).offset(skip).limit(limit))
    tasks = result.scalars().all()
    return tasks