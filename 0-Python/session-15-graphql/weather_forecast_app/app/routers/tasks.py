# app/routers/tasks.py

from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import select
from app.schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskWithWeather,
    UserCreate, UserResponse
)
from app.models import Task, User
from app.dependency import DBSession, ForecastClientDep


# Task Router

router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.post('/', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: DBSession # create independent session for each request, ensure db operation independence 
):
    """
    Create a new task
    Steps:
    1. Validate that the user exists
    2. Create task with provided data
    3. Save to database and return created task
    
    Args:
        task: TaskCreate schema with task data
        db: Database session dependency
        
    Returns:
        TaskResponse: Created task with generated ID
        
    Raises:
        HTTPException 404: If user does not exist
    """
    # Check if user exists before creating task
    user = db.get(User, task.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    # Create new task instance
    db_task = Task(
        title=task.title,
        content=task.content,
        city=task.city,
        user_id=task.user_id
    )
    
    # Add to database session
    db.add(db_task)
    
    # Commit transaction to save changes
    db.commit()
    
    # Refresh to get auto-generated fields (id, timestamps)
    db.refresh(db_task)
    
    return db_task


@router.get('/', response_model=list[TaskResponse])
def get_tasks(
    db: DBSession,
    user_id: int | None = Query(None, description="Filter tasks by user ID"),
    city: str | None = Query(None, description="Filter tasks by city name (case-insensitive)")
):
    """
    Get all tasks with optional filtering
    Supports filtering by:
    - user_id: Get tasks belonging to a specific user
    - city: Get tasks in a specific city (case-insensitive match)
    
    Examples:
        GET /tasks - Get all tasks
        GET /tasks?user_id=1 - Get tasks for user 1
        GET /tasks?city=tokyo - Get tasks in Tokyo (matches "Tokyo", "TOKYO", "tokyo")
        GET /tasks?user_id=1&city=london - Get tasks for user 1 in London
    
    Args:
        db: Database session dependency
        user_id: Optional user ID filter
        city: Optional city name filter
        
    Returns:
        list[TaskResponse]: List of tasks matching the filters
    """
    # Start with base query selecting all tasks
    statement = select(Task)
    
    # Apply user_id filter if provided
    if user_id is not None:
        statement = statement.where(Task.user_id == user_id)
    
    # Apply city filter if provided
    # ilike() performs case-insensitive matching (PostgreSQL ILIKE)
    if city is not None:
        statement = statement.where(Task.city.ilike(city))

    
    
    # Execute query and get all results
    tasks = db.exec(statement).all()

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='City not found'
        )

    return tasks


@router.get('/{task_id}', response_model=TaskWithWeather)
async def get_task(
    task_id: int,
    db: DBSession,
    forecast_client: ForecastClientDep
):
    """
    Get a single task with weather information (ASYNC)
    
    This endpoint is async because it makes external API calls
    
    Workflow:
    1. Retrieve task from database
    2. Get coordinates for the task's city
    3. Fetch current weather using coordinates
    4. Return task data with weather information
    
    Args:
        task_id: ID of the task to retrieve
        db: Database session dependency
        forecast_client: Weather forecast client dependency
        
    Returns:
        TaskWithWeather: Task data including current weather
        
    Raises:
        HTTPException 404: If task not found
        HTTPException 404: If city not found in geocoding API
        HTTPException 500: If weather service fails
    """
    # Retrieve task by ID
    task = db.get(Task, task_id)
    
    # Return 404 if task doesn't exist
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Fetch weather data asynchronously
    try:
        # Call weather API to get forecast for task's city
        weather_data = await forecast_client.get_forecast_for_city(task.city)
    except ValueError:
        # City not found in geocoding API
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    except Exception as e:
        # Other errors (network issues, API down, etc.)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Weather service error: {str(e)}"
        )
    
    # Build response combining task data and weather
    return {
        "id": task.id,
        "title": task.title,
        "content": task.content,
        "city": task.city,
        "user_id": task.user_id,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "weather": weather_data
    }


@router.put('/{task_id}', response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: DBSession
):
    """
    Update an existing task
    
    Only provided fields will be updated (partial update)
    If user_id is being changed, validates that new user exists
    
    Args:
        task_id: ID of the task to update
        task_update: TaskUpdate schema with fields to update
        db: Database session dependency
        
    Returns:
        TaskResponse: Updated task data
        
    Raises:
        HTTPException 404: If task not found
        HTTPException 404: If new user_id doesn't exist
    """
    # Get existing task
    task = db.get(Task, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # If updating user_id, verify new user exists
    if task_update.user_id is not None:
        user = db.get(User, task_update.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    
    # Get only the fields that were provided (exclude unset fields)
    update_data = task_update.model_dump(exclude_unset=True)
    
    # Update each provided field
    for key, value in update_data.items():
        setattr(task, key, value)
    
    # Update the updated_at timestamp
    from datetime import datetime
    task.updated_at = datetime.now()
    
    # Save changes to database
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: DBSession
):
    """
    Delete a task
    
    Args:
        task_id: ID of the task to delete
        db: Database session dependency
        
    Returns:
        None (204 No Content status)
        
    Raises:
        HTTPException 404: If task not found
    """
    # Get task to delete
    task = db.get(Task, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Delete from database
    db.delete(task)
    db.commit()
    
    # Return None for 204 No Content response
    return None


# User Router

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: DBSession
):
    """
    Create a new user
    
    Args:
        user: UserCreate schema with user data
        db: Database session dependency
        
    Returns:
        UserResponse: Created user with generated ID
    """
    # Create new user instance
    db_user = User(name=user.name)
    
    # Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@user_router.get('/', response_model=list[UserResponse])
def get_users(db: DBSession):
    """
    Get all users
    
    Args:
        db: Database session dependency
        
    Returns:
        list[UserResponse]: List of all users
    """
    # Select all users from database
    statement = select(User)
    users = db.exec(statement).all()
    
    return users


@user_router.get('/{user_id}', response_model=UserResponse)
def get_user(
    user_id: int,
    db: DBSession
):
    """
    Get a specific user by ID
    
    Args:
        user_id: ID of the user to retrieve
        db: Database session dependency
        
    Returns:
        UserResponse: User data
        
    Raises:
        HTTPException 404: If user not found
    """
    # Get user by ID
    user = db.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: DBSession
):
    """
    Delete a user
    
    Note: This will also delete all tasks belonging to this user
    due to cascade_delete=True in the relationship
    
    Args:
        user_id: ID of the user to delete
        db: Database session dependency
        
    Returns:
        None (204 No Content status)
        
    Raises:
        HTTPException 404: If user not found
    """
    # Get user to delete
    user = db.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Delete user (and cascade delete their tasks)
    db.delete(user)
    db.commit()
    
    return None