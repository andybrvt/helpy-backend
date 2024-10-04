from fastapi import HTTPException
from crud.crud_task import create_task
from crud.crud_alexa_device import get_room_and_community_from_alexa  # Import the helper function

async def handle_help_intent(data, db):
    task = data['request']['intent']['slots'].get('Task', {}).get('value')
    device_id = data['context']['System']['device']['deviceId']  # Extract the Alexa device ID from the request

    if task and device_id:
        try:
            # Use the helper function to get the room, community, and AlexaDevice ID from the Alexa device_id
            room, community, alexa_device_id = await get_room_and_community_from_alexa(db, device_id)

            if not room or not community:
                raise HTTPException(status_code=404, detail="Room or Community not found")

            # Create the task in the database, associating it with the Alexa device, room, and community
            await create_task(db, task, alexa_device_id=alexa_device_id, community_id=community.id, room_id=room.id)
            return {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": f"Task '{task}' has been created and linked to the correct room and Alexa device."
                    },
                    "shouldEndSession": False
                }
            }
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Error creating task")
    
    return await default_response()

async def default_response():
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "I'm not sure what you mean. How can I assist you today?"
            },
            "shouldEndSession": False
        }
    }
