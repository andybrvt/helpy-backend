from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import Community, User
from schemas.community import CommunityCreate, CommunityUpdate
from crud.crud_user import update_user, get_user  # Import your existing update_user function
from schemas.user import UserUpdate  # Import the UserUpdate schema
from fastapi import HTTPException
import random
import string



# Helper function to generate a unique 5-character alphanumeric PIN
async def generate_unique_pin(db: AsyncSession):
    while True:
        pin_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        # Ensure the PIN is unique across all communities
        existing_community = await db.execute(select(Community).filter(Community.pin_code == pin_code))
        if not existing_community.scalars().first():
            return pin_code  # Return the unique pin_code


async def create_community(db: AsyncSession, community: CommunityCreate, creator_id: int):
    try:
        # Step 1: Generate a unique pin for the new community
        pin_code = await generate_unique_pin(db)


        # Step 1: Create and commit the new community
        new_community = Community(
            name=community.name,
            address=community.address,
            email=community.email,
            phone_number=community.phone_number,
            created_by_id=creator_id,  # Set the creator's ID
            pin_code=pin_code  # Assign the generated pin_code

        )
        db.add(new_community)
        await db.commit()  # Commit to generate new_community.id
        await db.refresh(new_community)  # Now new_community.id will have the generated value

        # Step 2: Retrieve and update the user using selectinload to fetch related community
        creator = await get_user(db, creator_id)
        print(creator.id)
        
        if creator:
            creator.community_id = new_community.id
            creator.role = 'manager'  # Update the role to 'manager'
            db.add(creator)
            await db.commit()  # Commit the user changes
            await db.refresh(creator)  # Refresh the creator object

        
        
        return new_community

    except Exception as e:
        await db.rollback()  # Rollback the transaction in case of an error
        raise e


# Get a community by ID
async def get_community_by_id(db: AsyncSession, community_id: int):
    stmt = select(Community).filter(Community.id == community_id)
    result = await db.execute(stmt)
    return result.scalars().first()

# Get all communities with pagination
async def get_communities(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Community).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# Update a community
async def update_community(db: AsyncSession, community_id: int, community_update: CommunityUpdate):
    db_community = await get_community_by_id(db, community_id)
    if not db_community:
        return None
    for key, value in community_update.dict(exclude_unset=True).items():
        setattr(db_community, key, value)
    await db.commit()
    await db.refresh(db_community)
    return db_community

# Delete a community
async def delete_community(db: AsyncSession, community_id: int):
    db_community = await get_community_by_id(db, community_id)
    if not db_community:
        return None
    await db.delete(db_community)
    await db.commit()
    return db_community
