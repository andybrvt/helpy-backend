from fastapi import HTTPException
from crud.crud_task import create_task

async def handle_help_intent(data, db):
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
