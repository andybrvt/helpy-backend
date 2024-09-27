from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import Community
from schemas.community import CommunityCreate, CommunityUpdate

# Create a new community
async def create_community(db: AsyncSession, community: CommunityCreate, creator_id: int):
    new_community = Community(
        name=community.name,
        address=community.address,
        email=community.email,
        phone_number=community.phone_number,
        created_by_id=creator_id  # Set the creator's ID
    )
    db.add(new_community)
    await db.commit()
    await db.refresh(new_community)
    return new_community

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
