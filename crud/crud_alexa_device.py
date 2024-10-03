from sqlalchemy.ext.asyncio import AsyncSession
from models.models import AlexaDevice  # Adjusted import to point to models folder
from schemas.alexadevice import AlexaDeviceCreate, AlexaDeviceUpdate  # Adjusted import to point to schema folder
from sqlalchemy.future import select

# Create a new Alexa device (async version)
async def create_alexa_device(db: AsyncSession, device: AlexaDeviceCreate):
    db_device = AlexaDevice(
        device_id=device.device_id,
        room_id=device.room_id,
        community_id=device.community_id,
        status=device.status,
        last_synced=device.last_synced,
        last_request=device.last_request,
        total_number_requested=device.total_number_requested
    )
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device

# Get an Alexa device by device_id (async version)
async def get_alexa_device_by_id(db: AsyncSession, device_id: str):
    result = await db.execute(select(AlexaDevice).filter(AlexaDevice.device_id == device_id))
    return result.scalars().first()

# Get all Alexa devices for a room (async version)
async def get_alexa_devices_by_room(db: AsyncSession, room_id: int):
    result = await db.execute(select(AlexaDevice).filter(AlexaDevice.room_id == room_id))
    return result.scalars().all()

# Update an Alexa device (async version)
async def update_alexa_device(db: AsyncSession, device_id: str, updates: AlexaDeviceUpdate):
    result = await db.execute(select(AlexaDevice).filter(AlexaDevice.device_id == device_id))
    db_device = result.scalars().first()
    if not db_device:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_device, key, value)
    await db.commit()
    await db.refresh(db_device)
    return db_device

# Delete an Alexa device (async version)
async def delete_alexa_device(db: AsyncSession, device_id: str):
    result = await db.execute(select(AlexaDevice).filter(AlexaDevice.device_id == device_id))
    db_device = result.scalars().first()
    if db_device:
        await db.delete(db_device)
        await db.commit()
    return db_device


# Get all Alexa devices (global view)
async def get_all_alexa_devices(db: AsyncSession):
    result = await db.execute(select(AlexaDevice))
    return result.scalars().all()

# Get Alexa devices for a specific community
async def get_alexa_devices_by_community(db: AsyncSession, community_id: int):
    result = await db.execute(select(AlexaDevice).filter(AlexaDevice.community_id == community_id))
    return result.scalars().all()
