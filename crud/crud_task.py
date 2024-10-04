from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Task

async def create_task(db: AsyncSession, task_type: str, alexa_device_id: int, community_id: int, room_id: int, description: str = None):
    new_task = Task(
        title=task_type,
        description=description,
        status="pending",
        priority_score=1,  # Default priority score
        alexa_device_id=alexa_device_id,  # Associate Alexa device
        community_id=community_id,  # Associate community
        room_id=room_id  # Associate room
    )
    
    db.add(new_task)
    await db.commit()  # Use await with async functions
    await db.refresh(new_task)
    return new_task