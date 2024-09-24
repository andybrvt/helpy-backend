from sqlalchemy.orm import Session
from models.models import Task  # Import your Task model

def create_task(db: Session, task_type: str, description: str = None):
    new_task = Task(
        title=task_type,
        description=description,
        status="pending",
        priority_score=1  # Assign default priority score 
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task