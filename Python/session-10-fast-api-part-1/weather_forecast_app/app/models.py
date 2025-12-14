# app/models.py

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class User(SQLModel, table=True):
    """
    User model representing a user in the system
    Each user can have multiple tasks
    """
    __tablename__ = 'users'  # type: ignore
    
    # Primary key, auto-incremented
    id: int | None = Field(default=None, primary_key=True)
    
    # User's name, required field with max length
    name: str = Field(max_length=100)
    
    # Timestamp when user was created
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relationship: One user has many tasks
    # cascade_delete=True means deleting a user will also delete their tasks
    tasks: list['Task'] = Relationship(
        back_populates='user',
        cascade_delete=True
    )


class Task(SQLModel, table=True):
    """
    Task model representing a task with weather information
    Each task belongs to a user and has a city for weather lookup
    """
    __tablename__ = 'tasks'  # type: ignore
    
    # Primary key, auto-incremented
    id: int | None = Field(default=None, primary_key=True)
    
    # Task title, minimum 3 characters required (validated in schema)
    title: str = Field(max_length=200, index=True)
    
    # Task content/description, required field
    content: str
    
    # City name for weather lookup, indexed for faster filtering
    city: str = Field(max_length=100, index=True)
    
    # Foreign key referencing users table
    # Index added for faster JOIN operations
    user_id: int = Field(foreign_key='users.id', index=True)
    
    # Timestamps for tracking creation and updates
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationship: Task belongs to one user
    user: User = Relationship(back_populates='tasks')