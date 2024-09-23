from fastapi import APIRouter, Request

# to start testingg with alexa, activate ngrok http 8000

router = APIRouter()

@router.post("/alexa-request-help")
async def alexa_request_help(request: Request):
    data = await request.json()
    # Process the request here
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Your request has been logged."
            },
            "shouldEndSession": True
        }
    }