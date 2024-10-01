from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.crud_alexa_device import create_alexa_device, get_alexa_device_by_id
from crud.crud_room import get_room_by_number
from schemas.alexadevice import AlexaDeviceCreate
from database_configs.db import get_db  # Adjust path to your database module

router = APIRouter()

@router.post("/alexa-register-device")
async def alexa_register_device(request: Request, db: Session = Depends(get_db)):
    try:
        # Parse the request data
        data = await request.json()
        
        # Extract device ID from Alexa request
        device_id = data['context']['System']['device']['deviceId']
        
        # Extract room number or other relevant info (assumes room number is a slot)
        room_number = data['request']['intent']['slots']['RoomNumber']['value']
        
        # Optionally, extract the PIN (if you're using one)
        pin = data['request']['intent']['slots'].get('PIN', {}).get('value')
        
        # Logic to check if the room number is valid and map it to a room ID
        # For example:
        room = await get_room_by_number(db, room_number)  # Implement get_room_by_number function
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        # Check if the device is already registered
        existing_device = get_alexa_device_by_id(db, device_id)
        if existing_device:
            raise HTTPException(status_code=400, detail="Device already registered")
        
        # Create a new Alexa device and associate it with the room
        alexa_device = AlexaDeviceCreate(
            device_id=device_id,
            room_id=room.id,
            community_id=room.community_id  # Assuming room has community_id
        )
        create_alexa_device(db, alexa_device)
        
        # Return a success response to Alexa
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": f"Device registered successfully for Room {room_number}."
                },
                "shouldEndSession": False
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
