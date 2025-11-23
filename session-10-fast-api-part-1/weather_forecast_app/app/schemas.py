# app/schemas.py

from pydantic import BaseModel, Field
from datetime import datetime



class UserCreate(BaseModel):
    """
    Schema for creating a new user
    Validates that name is not empty
    """
    name: str = Field(..., min_length=1, max_length=100,description="User name, required")


class UserResponse(BaseModel):
    """
    Schema for user response
    Returns user data with ID and timestamps
    """
    id: int
    name: str
    created_at: datetime
    
    class Config:
        # Allow creating Pydantic model from SQLModel/ORM object
        from_attributes = True




class TaskBase(BaseModel):
    """
    Base schema with common task fields
    Contains validation rules for all task operations
    """
    # Title must be at least 3 characters
    title: str = Field(..., min_length=3, max_length=200, description="Task title, minimum 3 characters")
    
    # Content cannot be empty
    content: str = Field(..., min_length=1, description="Task content, required")
    
    # City name for weather lookup, cannot be empty
    city: str = Field(..., min_length=1, max_length=100, description="City name for weather lookup, required")


class TaskCreate(TaskBase):
    """
    Schema for creating a new task
    Includes user_id to associate task with a user
    """
    user_id: int = Field(..., description="ID of the user who owns this task")


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task
    All fields are optional - only provided fields will be updated
    """
    title: str | None = Field(None, min_length=3, max_length=200)
    content: str | None = Field(None, min_length=1)
    city: str | None = Field(None, min_length=1, max_length=100)
    user_id: int | None = None


class TaskResponse(TaskBase):
    """
    Schema for task response without weather data
    Used when listing multiple tasks
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True



class WeatherData(BaseModel):
    """
    Schema for weather information from Open-Meteo API
    Contains current weather conditions
    """
    temperature: float  # Temperature in Celsius
    windspeed: float    # Wind speed in km/h
    weathercode: int    # WMO Weather interpretation code
    time: str           # ISO 8601 timestamp


class TaskWithWeather(TaskResponse):
    """
    Schema for task response including weather data
    Used when retrieving a single task with weather information
    Extends TaskResponse and adds weather field
    """
    weather: WeatherData