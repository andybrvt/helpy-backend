from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User
from crud.crud_alexa_device import (
    get_all_alexa_devices,
    get_alexa_devices_by_community
)
from database_configs.db import get_db  # Use the correct path to your database module
from auth.dependencies import get_current_user  # Your authentication dependency
from schemas.alexadevice import AlexaDeviceResponse  # Import your Pydantic response schema



router = APIRouter()

# Route to get all registered Alexa devices (global view)
@router.get("/alexa-devices/", response_model=list[AlexaDeviceResponse], status_code=status.HTTP_200_OK)
async def get_all_devices(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only allow 'manager' or 'admin' roles to access all devices
    if current_user.role not in ['manager', 'admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view Alexa devices.")

    devices = await get_all_alexa_devices(db)
    if not devices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Alexa devices found.")
    return devices

# Route to get Alexa devices for a specific community (with rooms)
@router.get("/communities/{community_id}/alexa-devices/", response_model=list[AlexaDeviceResponse], status_code=status.HTTP_200_OK)
async def get_devices_for_community(
    community_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure the current user is a manager of the community or has 'admin' role
    if current_user.role not in ['manager', 'admin'] or current_user.community_id != community_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view Alexa devices for this community.")

    devices = await get_alexa_devices_by_community(db, community_id)
    if not devices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Alexa devices found for community {community_id}.")
    return devices
