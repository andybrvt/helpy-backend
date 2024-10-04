from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession  # Using AsyncSession for async DB operations
from typing import List
from schemas.room import RoomCreate, RoomUpdate, RoomResponse, RoomAlexaStatusResponse  # Adjust paths as needed
from models.models import User  # Import the User model for authentication
from crud.crud_room import create_room, get_room_by_id, get_rooms_for_community, update_room, delete_room  # Adjust paths as needed
from auth.dependencies import get_current_user  # Import the authentication dependency
from database_configs.db import get_db  # Ensure this is the correct path to your DB config
from schemas.alexadevice import AlexaDeviceResponse


router = APIRouter()

# Route to create a new room (auth required)
@router.post("/rooms/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_new_room(
    room: RoomCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not current_user.community_id:
        raise HTTPException(status_code=400, detail="User is not associated with any community")

    # Pass community_id as a separate argument to the CRUD function
    created_room = await create_room(db=db, room=room, community_id=current_user.community_id)
    return RoomResponse.from_orm(created_room)

# Route to get a room by its ID (auth required)
@router.get("/rooms/{room_id}", response_model=RoomResponse)
async def read_room(room_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_room = await get_room_by_id(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return RoomResponse.from_orm(db_room)

# Route to get all rooms for the current user's community (auth required)
@router.get("/communities/{community_id}/rooms", response_model=List[RoomResponse])
async def read_rooms_for_community(
    community_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Fetch all rooms for the specified community
    rooms = await get_rooms_for_community(db=db, community_id=community_id)
    return [RoomResponse.from_orm(room) for room in rooms]

# Route to update an existing room (auth required)
@router.put("/rooms/{room_id}", response_model=RoomResponse)
async def update_existing_room(
    room_id: int, 
    room: RoomUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Fetch the room from the database
    db_room = await get_room_by_id(db=db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    # Ensure the room belongs to the current user's community
    if db_room.community_id != current_user.community_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this room")

    # Update the room in the database
    updated_room = await update_room(db=db, room_id=room_id, room_update=room)
    return RoomResponse.from_orm(updated_room)

# Route to delete a room (auth required)
@router.delete("/rooms/{room_id}", response_model=RoomResponse)
async def delete_existing_room(
    room_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Fetch the room from the database
    db_room = await get_room_by_id(db=db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    # Ensure the room belongs to the current user's community
    if db_room.community_id != current_user.community_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this room")

    # Delete the room from the database
    deleted_room = await delete_room(db=db, room_id=room_id)
    return RoomResponse.from_orm(deleted_room)

@router.get("/my-community/rooms", response_model=List[RoomResponse])
async def read_rooms_for_logged_in_user_community(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Fetch all rooms for the community associated with the logged-in user
    community_id = current_user.community_id
    rooms = await get_rooms_for_community(db=db, community_id=community_id)
    # Manually convert each room and its alexa_devices
    room_responses = []
    for room in rooms:
        alexa_devices_response = [AlexaDeviceResponse.from_orm(device) for device in room.alexa_devices]
        
        room_responses.append(RoomResponse(
            id=room.id,
            room_number=room.room_number,
            community_id=room.community_id,
            resident_id=room.resident_id,
            floor_number=room.floor_number,
            room_type=room.room_type,
            alexa_devices=alexa_devices_response  # Convert the alexa devices here
        ))

    return room_responses


@router.get("/rooms/{room_id}/alexa-status", response_model=RoomAlexaStatusResponse)
async def check_alexa_device_status(room_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Fetch the room by ID
    db_room = await get_room_by_id(db, room_id=room_id)
    
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Ensure the room belongs to the current user's community
    if db_room.community_id != current_user.community_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this room")

    # Check if there are any Alexa devices linked to the room
    alexa_devices = db_room.alexa_devices
    alexa_connected = bool(alexa_devices)  # True if there are Alexa devices linked

    return RoomAlexaStatusResponse(
        room_id=db_room.id,
        alexa_connected=alexa_connected
    )
