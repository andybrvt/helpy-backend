from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func, Float, Table
from sqlalchemy.orm import relationship
from database_configs.db import Base
from enum import Enum as PyEnum


# psql 
# psql -h localhost -U andyle -d helpydb



# User is the subclass of Base, it inherits all the behaviors and attributes
class User(Base):
    #defines the name of the table in the postgresql
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum('resident', 'staff', 'administrator', 'corporate_leader', 'care_staff', 'manager', name='user_role'))
    staff_id = Column(String, index=True, nullable=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    # Relationship with Task (Many-to-Many)
    tasks = relationship("Task", secondary="task_assignments", back_populates="assigned_users")

    tasks_completed = relationship("Task", back_populates="completed_by")

    # Task one to many with communities
    community_id = Column(Integer, ForeignKey("communities.id", use_alter=True), nullable=True)
    community = relationship("Community", back_populates="users", foreign_keys=[community_id])

    room = relationship("Room", back_populates="resident", uselist=False)  # One-to-one relationship
    
    # many to many relationship with notifications
    notifications = relationship("Notification", secondary="notification_recipients", back_populates="recipients")

    caregiver_logs = relationship("CaregiverLog", foreign_keys="[CaregiverLog.caregiver_id]", back_populates="caregiver")
    received_care_logs = relationship("CaregiverLog", foreign_keys="[CaregiverLog.resident_id]", back_populates="resident")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    # many to many relationship with User (assigned caregivers) 
    assigned_users = relationship("User", secondary="task_assignments", back_populates="tasks")

    # before task was done...
    response_date_time= Column(DateTime(timezone=True), nullable=True, index=True)
    # Response time (in minutes, calculated from call to showing up -> confirmed)
    response_time = Column(Float, nullable=True)  # Float to allow partial minutes (e.g., 5.5 minutes)


    # When tasks was done...
    # Foreign Key to User who confirmed the task (optional field)
    completed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    completed_by = relationship("User", foreign_keys=[completed_by_id], back_populates="tasks_completed")
    # Task completion date/time (when the task was acknowledged)
    completion_time = Column(DateTime(timezone=True), nullable=True, index=True)
    # Task time length (in minutes, calculated from response_date_time to completion_time)
    task_time_length = Column(Float, nullable=True, default=0.0)  # Same reason as above


    # Task status (enum)
    status = Column(Enum('pending', 'in_progress', 'completed', name='task_status'), default='pending', nullable=False)
    # Priority score (integer value for urgency)
    priority_score = Column(Integer, nullable=False, default=1)  # Default priority score

    

    # Timestamps for task creation and last update
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)
    
    
    # Foreign Key to Community table
    #the foreign key will signify the one to many relationship
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=True)
    community = relationship("Community", back_populates="tasks")

    # Foreign Key to AlexaDevice table, one alexa can have many tasks
    alexa_device_id = Column(Integer, ForeignKey("alexa_devices.id"), nullable=True)
    alexa_device = relationship("AlexaDevice", back_populates="tasks_requested")

    notifications = relationship("Notification", back_populates="task")

    # this is a one to many relationships     
    caregiver_logs = relationship("CaregiverLog", back_populates="task")



#set up the community model
class Community(Base):

    __tablename__ = "communities"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    # Community details
    name = Column(String, nullable=False, index=True)  # Community name, required and indexed for fast search
    address = Column(String, nullable=False)  # Community address
    email = Column(String, nullable=True)  # Optional contact info (email, phone, etc.)
    phone_number = Column(String, nullable=True)

    # Foreign Key to User (Creator)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = relationship("User", foreign_keys=[created_by_id])

    # One-to-Many relationship with Task
    tasks = relationship("Task", back_populates="community")

    # One-to-Many relationship with User (if users belong to specific communities)
    users = relationship("User", back_populates="community", foreign_keys="[User.community_id]")

    # one to many relationship with room
    rooms = relationship("Room", back_populates="community")

     # Automatically set created_at when a new record is inserted
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)



class AlexaDevice(Base):
    __tablename__ = "alexa_devices"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    # Unique identifier for the Alexa device (provided by the device)
    device_id = Column(String, nullable=False, unique=True, index=True)  # Unique and indexed for fast lookup

    # Foreign Key to Room table
    # one to many relationship with room, a room can have multiple alexa's i guess
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    room = relationship("Room", back_populates="alexa_devices")
    

    # Status of the device (e.g., active, inactive, offline)
    status = Column(String, nullable=False, default="active")  # Default status is 'active'

    # Timestamp of the last synchronization with the system
    last_synced = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamp of the last request made by the device
    last_request = Column(DateTime(timezone=True), nullable=True)

    # Total number of requests made by this device
    total_number_requested = Column(Integer, nullable=False, default=0)

    # One-to-Many relationship with Task (tasks requested by this device)
    tasks_requested = relationship("Task", back_populates="alexa_device")

    
class Room(Base):
    __tablename__ = "rooms"
     # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Room number or name
    room_number = Column(String, nullable=False, index=True, unique=True)
    
    # Foreign Key to Community table
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=False)
    community = relationship("Community", back_populates="rooms")

    # Optional Foreign Key to Resident User Profile (if a specific resident is linked to the room) 
    resident_id = Column(Integer, ForeignKey("users.id"), nullable=True, index = True)
    resident = relationship("User", back_populates="room", foreign_keys=[resident_id], uselist=False)
    
    # One-to-Many relationship with AlexaDevice
    alexa_devices = relationship("AlexaDevice", back_populates="room")
    
    # Optional fields for room properties
    floor_number = Column(Integer, nullable=True)  # Optional field to store the floor number
    room_type = Column(String, nullable=True)  # Optional field to store room type (e.g., single, shared)


class Notification(Base):
    __tablename__ = "notifications"
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Message content for the notification
    message = Column(String, nullable=False)

    # Many-to-Many relationship with User (recipients of the notification)
    recipients = relationship("User", secondary="notification_recipients", back_populates="notifications")
    
    # Foreign Key to Task (if this notification is related to a specific task)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    task = relationship("Task", back_populates="notifications")

    # Timestamp of when the notification was created
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status of the notification (e.g., sent, read, acknowledged)
    status = Column(Enum('sent', 'read', 'acknowledged', name='notification_status'), default='sent')


class CaregiverLog(Base):
    __tablename__ = "caregiver_logs"
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key to Task (if this log is related to a specific task)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    task = relationship("Task", back_populates="caregiver_logs")
    
    # Foreign Key to User (caregiver performing the action)
    caregiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    caregiver = relationship("User", foreign_keys=[caregiver_id])

    # Foreign Key to User (resident receiving care, if applicable)
    resident_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    resident = relationship("User", foreign_keys=[resident_id])
    
    # Action performed by the caregiver
    action = Column(String, nullable=False)  # Description of the action taken
    
    # Timestamp of the action
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Additional notes or observations
    notes = Column(String, nullable=True)

    # Status of the log entry
    status = Column(Enum('completed', 'pending_review', 'rejected', name='log_status'), default='completed')
    
    # Optional location field (e.g., room number)
    location = Column(String, nullable=True)

# Task Assignment (Many-to-Many relationship table)
task_assignments = Table(
    "task_assignments", 
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id"), primary_key=True)
)

# Many-to-Many association table between User and Notification
notification_recipients = Table(
    "notification_recipients",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("notification_id", Integer, ForeignKey("notifications.id"), primary_key=True)
)


