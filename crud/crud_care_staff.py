from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User
from schemas.user import UserCreate, UserUpdate
from auth.utils import get_password_hash

# Care Staff Role Filter
CARE_STAFF_ROLE = 'care_staff'  # Ensure this role is added to the Enum in your models

# Fetch a specific care staff by ID
async def get_care_staff_by_id(db: AsyncSession, user_id: int):
    stmt = select(User).filter(User.id == user_id, User.role == CARE_STAFF_ROLE)
    result = await db.execute(stmt)
    return result.scalars().first()

# Fetch a specific care staff by email
async def get_care_staff_by_email(db: AsyncSession, email: str):
    stmt = select(User).filter(User.email == email, User.role == CARE_STAFF_ROLE)
    result = await db.execute(stmt)
    return result.scalars().first()

# Fetch all care staff with pagination
async def get_care_staff(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(User).filter(User.role == CARE_STAFF_ROLE).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# Create a new care staff
async def create_care_staff(db: AsyncSession, user: UserCreate):
    # Hash the password before storing
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        role=CARE_STAFF_ROLE,
        hashed_password=hashed_password,
        community_id=user.community_id  # Assuming care staff is assigned to a community
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Update an existing care staff
async def update_care_staff(db: AsyncSession, user_id: int, user_update: UserUpdate):
    db_user = await get_care_staff_by_id(db, user_id)  # Check if the care staff exists
    if not db_user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Delete an existing care staff
async def delete_care_staff(db: AsyncSession, user_id: int):
    db_user = await get_care_staff_by_id(db, user_id)  # Check if the care staff exists
    if not db_user:
        return None
    await db.delete(db_user)
    await db.commit()
    return db_user
