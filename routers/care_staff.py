from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.care_staff import CareStaffCreate, CareStaffUpdate, CareStaffResponse
from models.models import User
from crud.crud_care_staff import (
    get_care_staff_by_id,
    get_care_staff,
    create_care_staff,
    update_care_staff,
    delete_care_staff,
)
from database_configs.db import get_db  # Use the correct path to your database module
from auth.dependencies import get_current_user
from sqlalchemy.future import select  # Import the select function for querying

CARE_STAFF_ROLE = 'care_staff'  # Ensure this role is added to the Enum in your models

router = APIRouter()

# Route to create a new care staff member
@router.post("/care_staff/", response_model=CareStaffResponse, status_code=status.HTTP_201_CREATED)
async def create_new_care_staff(
    care_staff: CareStaffCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if the current user is a manager and belongs to a community
    if current_user.role != 'manager' or not current_user.community_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only managers can add care staff.")

    # Assign the current user's community to the new care staff
    care_staff.community_id = current_user.community_id

    # Create the care staff
    created_care_staff = await create_care_staff(db=db, user=care_staff)
    return created_care_staff

# Route to get care staff by ID
@router.get("/care_staff/{care_staff_id}", response_model=CareStaffResponse)
async def read_care_staff(care_staff_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    care_staff = await get_care_staff_by_id(db=db, user_id=care_staff_id)
    if not care_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Care staff not found")
    return care_staff

# Route to get all care staff members with pagination
@router.get("/care_staff/", response_model=list[CareStaffResponse])
async def read_all_care_staff(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_care_staff(db=db, skip=skip, limit=limit)

# Route to update care staff information
@router.put("/care_staff/{care_staff_id}", response_model=CareStaffResponse)
async def update_care_staff_info(
    care_staff_id: int,
    care_staff_update: CareStaffUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if the current user is a manager
    if current_user.role != 'manager':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only managers can update care staff.")
    
    updated_care_staff = await update_care_staff(db=db, user_id=care_staff_id, user_update=care_staff_update)
    if not updated_care_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Care staff not found")
    return updated_care_staff

# Route to delete care staff
@router.delete("/care_staff/{care_staff_id}", response_model=CareStaffResponse)
async def delete_care_staff_info(
    care_staff_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if the current user is a manager
    if current_user.role != 'manager':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only managers can delete care staff.")
    
    deleted_care_staff = await delete_care_staff(db=db, user_id=care_staff_id)
    if not deleted_care_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Care staff not found")
    return deleted_care_staff


# Route to get all care staff members of a specific community
@router.get("/communities/{community_id}/care_staff/", response_model=list[CareStaffResponse])
async def read_care_staff_by_community(
    community_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if the current user is associated with the community
    if current_user.community_id != community_id and current_user.role != 'manager':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have access to this community's staff."
        )

    stmt = select(User).filter(User.community_id == community_id, User.role == CARE_STAFF_ROLE)
    result = await db.execute(stmt)
    care_staff_list = result.scalars().all()
    return care_staff_list