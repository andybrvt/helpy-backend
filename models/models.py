from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from ..db import Base


# User is the subclass of Base, it inherits all the behaviors and attributes
class User(Base):
    #defines the name of the table in the postgresql
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum('resident', 'staff', 'administrator', 'corporate_leader', name='user_role'))
    staff_id = Column(String, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    # Relationship with Task (Many-to-Many)
    tasks = relationship("Task", secondary="task_assignments", back_populates="assigned_users")
    tasks_completed = relationship("Task", back_populates="completed_by")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    # many to many relationship with User (assigned caregivers) 
    assigned_users = relationship("User", secondary="task_assignments", back_populates="tasks")

    # before task was done...
    response_date_time= Column(DateTime(timezone=True), nullable=True)
    # Response time (in minutes, calculated from call to showing up -> confirmed)
    response_time = Column(Float, nullable=True)  # Float to allow partial minutes (e.g., 5.5 minutes)


    # When tasks was done...
    # Foreign Key to User who confirmed the task (optional field)
    completed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    completed_by = relationship("User", foreign_keys=[completed_by_id])
    # Task confirmation time (when the task was acknowledged)
    completion_time = Column(DateTime(timezone=True), nullable=True)
    # Task time length (in minutes, calculated from response_date_time to completion_time)
    task_time_length = Column(Float, nullable=True)  # Same reason as above


    # Task status (enum)
    status = Column(Enum('pending', 'in_progress', 'completed', name='task_status'), default='pending')
    # Priority score (integer value for urgency)
    priority_score = Column(Integer, nullable=False, default=1)  # Default priority score

    

    # Timestamps for task creation and last update
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)
    
    
    # Foreign Key to Community table
    #the foreign key will signify the one to many relationship
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=False)
    community = relationship("Community", back_populates="tasks")
    


#set up the community model
   

# Task Assignment (Many-to-Many relationship table)
task_assignments = Table(
    "task_assignments", 
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id"), primary_key=True)
)



