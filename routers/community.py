from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database_configs.db import get_db  # Ensure this is the correct path to your DB config
from models.models import Community, User  # Import the Community model
from schemas.community import CommunityCreate, CommunityUpdate, CommunityResponse  # Import Community schemas
from crud.crud_community import (
    create_community, 
    get_communities, 
    get_community_by_id,
    update_community, 
    delete_community
)
from auth.dependencies import get_current_user  # Import the authentication dependency
from schemas.user import UserInDB  # Import the authenticated user model

# Initialize the router with auth dependency
router = APIRouter(dependencies=[Depends(get_current_user)])

# Route to create a new community (auth required)
@router.post("/communities/", response_model=CommunityResponse, status_code=status.HTTP_201_CREATED)
async def create_new_community(
    community: CommunityCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    if not db or not current_user:
        raise HTTPException(status_code=400, detail="Invalid session or user context")

    created_community = await create_community(db=db, community=community, creator_id=current_user.id)
    return created_community

# Route to get a community by ID (auth required)
@router.get("/communities/{community_id}", response_model=CommunityResponse)
async def get_community(community_id: int, db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    db_community = await get_community_by_id(db, community_id)
    if not db_community:
        raise HTTPException(status_code=404, detail="Community not found")
    return db_community

# Route to get a list of all communities (auth required)
@router.get("/communities/", response_model=List[CommunityResponse])
async def get_all_communities(
    skip: int = 0, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)  # Authentication dependency
):
    communities = await get_communities(db, skip=skip, limit=limit)
    return communities

# Route to update a community by ID (auth required)
@router.put("/communities/{community_id}", response_model=CommunityResponse)
async def update_existing_community(
    community_id: int, 
    community: CommunityUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_community = await get_community_by_id(db, community_id)
    if not db_community:
        raise HTTPException(status_code=404, detail="Community not found")
    updated_community = await update_community(db=db, community_id=community_id, community_update=community)
    return updated_community

# Route to delete a community by ID (auth required)
@router.delete("/communities/{community_id}", response_model=CommunityResponse)
async def delete_community_by_id(
    community_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_community = await get_community_by_id(db, community_id)
    if not db_community:
        raise HTTPException(status_code=404, detail="Community not found")
    deleted_community = await delete_community(db=db, community_id=community_id)
    return deleted_community


@router.get("/community/manager", response_model=CommunityResponse)
async def get_manager_community(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Check if the user is a manager
    if current_user.role != 'manager':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resource."
        )
    
    print('community id here')
    print(current_user.community_id)
    # Fetch the community associated with this manager
    community = await db.get(Community, current_user.community_id)
    
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found."
        )
    
    return community