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

    

    if not pin_code:
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "PIN code is required to register the device. Please provide a valid PIN."
                },
                "shouldEndSession": False
            }
        }

    # Fetch the community using the pin code
    community = await get_community_by_pin(db, pin_code)
    if not community:
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": f"No community found with the provided PIN code '{pin_code}'. Please try again."
                },
                "shouldEndSession": False
            }
        }

    # Fetch the room within the community
    room = await get_room_by_number(db, room_number, community.id)
    if not room:
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": f"Room '{room_number}' not found in the community. Please provide a valid room number."
                },
                "shouldEndSession": False
            }
        }

    # Check if the device is already registered
    existing_device = await get_alexa_device_by_id(db, device_id)
    if existing_device:
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "This device is already registered to a room. If you need to change the room, please contact support."
                },
                "shouldEndSession": False
            }
        }
    
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
