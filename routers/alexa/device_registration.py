from fastapi import HTTPException
from crud.crud_alexa_device import create_alexa_device, get_alexa_device_by_id
from crud.crud_room import get_room_by_number
from crud.crud_community import get_community_by_pin
from schemas.alexadevice import AlexaDeviceCreate

async def handle_register_device_intent(data, db):
    # Extract device ID from Alexa request
    print(data)

    device_id = data['context']['System']['device']['deviceId']

    # Extract room number from slots
    room_number = data['request']['intent']['slots']['room']['value']

    # Extract the PIN from slots
    pin_code = data['request']['intent']['slots']['PIN']['value']

    print(room_number)
    print(pin_code)

    if not pin_code:
        raise HTTPException(status_code=400, detail="PIN code is required")

    # Fetch the community using the pin code
    community = await get_community_by_pin(db, pin_code)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    # Fetch the room within the community
    room = await get_room_by_number(db, room_number, community.id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Check if the device is already registered
    existing_device = await get_alexa_device_by_id(db, device_id)
    if existing_device:
        raise HTTPException(status_code=400, detail="Device already registered")

    
    # Register the Alexa device
    alexa_device = AlexaDeviceCreate(
        device_id=device_id,
        room_id=room.id,
        community_id=community.id
    )
    await create_alexa_device(db, alexa_device)

    
    # Return a success response to Alexa
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": f"Device registered successfully for Room {room_number}."
            },
            "shouldEndSession": True
        }
    }
