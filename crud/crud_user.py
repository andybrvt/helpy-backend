from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User
from schemas.user import UserCreate, UserUpdate
from auth.utils import get_password_hash


async def get_user(db: AsyncSession, user_id: int):
    stmt = select(User).options(selectinload(User.community)).filter(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).filter(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    # Use the get_password_hash function to hash the password
    db_user = User(
        name=user.name, email=user.email, role=user.role, hashed_password=user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    db_user = await get_user(db, user_id)  # Await the async function
    if not db_user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)  # Await the async function
    if not db_user:
        return None
    await db.delete(db_user)
    await db.commit()
    return db_user