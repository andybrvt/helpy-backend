from sqlalchemy.orm import Session
from models.models import AlexaDevice  # Adjusted import to point to models folder
from schemas.alexadevice import AlexaDeviceCreate, AlexaDeviceUpdate  # Adjusted import to point to schema folder

# Create a new Alexa device
def create_alexa_device(db: Session, device: AlexaDeviceCreate):
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
    db.commit()
    db.refresh(db_device)
    return db_device

# Get an Alexa device by device_id
def get_alexa_device_by_id(db: Session, device_id: str):
    return db.query(AlexaDevice).filter(AlexaDevice.device_id == device_id).first()

# Get all Alexa devices for a room
def get_alexa_devices_by_room(db: Session, room_id: int):
    return db.query(AlexaDevice).filter(AlexaDevice.room_id == room_id).all()

# Update an Alexa device
def update_alexa_device(db: Session, device_id: str, updates: AlexaDeviceUpdate):
    db_device = db.query(AlexaDevice).filter(AlexaDevice.device_id == device_id).first()
    if not db_device:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_device, key, value)
    db.commit()
    db.refresh(db_device)
    return db_device

# Delete an Alexa device
def delete_alexa_device(db: Session, device_id: str):
    db_device = db.query(AlexaDevice).filter(AlexaDevice.device_id == device_id).first()
    if db_device:
        db.delete(db_device)
        db.commit()
    return db_device
