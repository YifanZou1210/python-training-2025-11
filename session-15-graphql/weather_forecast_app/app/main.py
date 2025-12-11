# app/main.py

from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers.tasks import router as tasks_router, user_router


# Create all database tables
# This reads all SQLModel classes with table=True and creates corresponding tables
SQLModel.metadata.create_all(engine)


# Initialize FastAPI application
app = FastAPI(
    title="Task Management API with Weather Forecast",
    description="A task management system that integrates weather forecasts for task locations",
    version="1.0.0"
)


# Register routers
# Include user endpoints (CRD operations)
app.include_router(user_router)

# Include task endpoints (CRUD operations with weather)
app.include_router(tasks_router)


@app.get('/')
def home():
    """
    Root endpoint
    Returns welcome message and available endpoints
    """
    return {
        'message': 'Task Management API with Weather Forecast',
        'docs': '/docs',
        'endpoints': {
            'users': '/users',
            'tasks': '/tasks'
        }
    }


@app.get('/health')
def health_check():
    """
    Health check endpoint
    Used to verify the API is running
    """
    return {'status': 'ok'}