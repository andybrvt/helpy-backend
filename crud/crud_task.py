from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Task

async def create_task(db: AsyncSession, task_type: str, description: str = None):
    new_task = Task(
        title=task_type,
        description=description,
        status="pending",
        priority_score=1  # Assign default priority score
    )
    print(new_task)
    db.add(new_task)
    await db.commit()  # Use await with async functions
    await db.refresh(new_task)
    return new_task
