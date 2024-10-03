from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database_configs.db import get_db  # Use the correct path to your database module
from crud.crud_task import create_task  # Import the task creation function
from .help_response import handle_help_intent  # Import the help response
from .device_registration import handle_register_device_intent  # Import device registration handler



router = APIRouter()

@router.post("/actions")  # This will be accessible at /alexa/actions
async def alexa_actions(request: Request, db: AsyncSession = Depends(get_db)):
    print('data json conversion')
    data = await request.json()
    
    request_type = data['request']['type']
    print("Request type:", request_type)

    if request_type == "LaunchRequest":
        print('Handling LaunchRequest')
        return await handle_launch_request()
    elif request_type == "IntentRequest":
        print('Handling IntentRequest')
        return await handle_intent_request(data, db)
    else:
        print('Unhandled request type')
        return await default_response()
   

async def handle_launch_request():
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "How can I assist you today?"
            },
            "shouldEndSession": False
        }
    }

async def handle_intent_request(data, db):
    intent_name = data['request']['intent']['name']

    if intent_name == "RequestHelpIntent":
        return await handle_help_intent(data, db)  # Delegate to help_response.py

        


        """
             task = data['request']['intent']['slots'].get('Task', {}).get('value')
        if task:
            try:
                # Create the task in the database
                print('do you get here ', task)
                await create_task(db, task)
                return {
                    "version": "1.0",
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": f"Task '{task}' has been created. We'll assist you shortly."
                        },
                        "shouldEndSession": False
                    }
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail="Error creating task")
    

        """
    
    elif intent_name == "RegisterDeviceIntent":
        return await handle_register_device_intent(data, db)

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


"""
Register this device with room {room} and PIN {PIN}

room: 1204

PIN: MSTD4

"""