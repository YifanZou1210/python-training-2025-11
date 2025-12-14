# app/data_init.py

from sqlmodel import SQLModel, Session, select
from .database import engine
from .models import User, Task


def create_tables():
    """
    Create all database tables
    This function should be called before inserting any data
    """

    SQLModel.metadata.create_all(engine)


# Create tables first
create_tables()


# Insert initial data
with Session(engine) as session:
    # Check if data already exists to avoid duplicates
    statement = select(User)
    existing_users = session.exec(statement).all()
    
    if len(existing_users) > 0:
        print('✓ Data already exists, skipping initialization')
    else:
        # Create first user
        user1 = User(name='Alice')
        session.add(user1)
        session.commit()
        session.refresh(user1)
        
        print(f'Created user {user1.id}: {user1.name}')
        
        # Create second user
        user2 = User(name='Bob')
        session.add(user2)
        session.commit()
        session.refresh(user2)
        
        print(f'Created user {user2.id}: {user2.name}')
        
        # Create tasks for users
        if user1.id:
            # Task 1: Alice's task in Tokyo
            task1 = Task(
                title="Team meeting",
                content="Discuss Q4 objectives",
                city="Tokyo",
                user_id=user1.id
            )
            session.add(task1)
            
            # Task 2: Alice's task in London
            task2 = Task(
                title="Visit office",
                content="Quarterly review meeting",
                city="London",
                user_id=user1.id
            )
            session.add(task2)
            
            session.commit()
            print(f'Created 2 tasks for user {user1.name}')
        
        if user2.id:
            # Task 3: Bob's task in Paris
            task3 = Task(
                title="Conference talk",
                content="Present new features",
                city="Paris",
                user_id=user2.id
            )
            session.add(task3)
            
            session.commit()
            print(f'Created 1 task for user {user2.name}')
        
        print('✓ Test data initialization complete!')