from sqlalchemy.ext.asyncio import AsyncSession  # Ensure you're using AsyncSession
from models.models import Room
from schemas.room import RoomCreate, RoomUpdate, RoomResponse  # Adjust paths as needed
from sqlalchemy.future import select

# Create a new room
async def create_room(db: AsyncSession, room: RoomCreate, community_id: int):
    db_room = Room(
        room_number=room.room_number,
        community_id=community_id,  # Pass community_id separately
        resident_id=room.resident_id,
        floor_number=room.floor_number,
        room_type=room.room_type
    )
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room

# Get a room by ID
async def get_room_by_id(db: AsyncSession, room_id: int):
    result = await db.execute(select(Room).filter(Room.id == room_id))
    return result.scalars().first()

# Get all rooms for a community
async def get_rooms_for_community(db: AsyncSession, community_id: int):
    result = await db.execute(select(Room).filter(Room.community_id == community_id))
    return result.scalars().all()

# Update a room
async def update_room(db: AsyncSession, room_id: int, room: RoomUpdate):
    db_room = await get_room_by_id(db, room_id)
    if db_room is None:
        return None

    db_room.room_number = room.room_number
    db_room.resident_id = room.resident_id
    db_room.floor_number = room.floor_number
    db_room.room_type = room.room_type

    await db.commit()
    await db.refresh(db_room)
    return db_room

# Delete a room
async def delete_room(db: AsyncSession, room_id: int):
    db_room = await get_room_by_id(db, room_id)
    if db_room is None:
        return None

    await db.delete(db_room)
    await db.commit()
    return db_room

# Get a room by room number and community ID
async def get_room_by_number(db: AsyncSession, room_number: str, community_id: int):
    result = await db.execute(select(Room).filter(Room.room_number == room_number, Room.community_id == community_id))
    return result.scalars().first()

