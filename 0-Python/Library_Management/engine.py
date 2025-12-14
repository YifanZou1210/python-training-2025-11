from sqlalchemy import create_engine 
engine = create_engine(
    'postgresql://postgres:mypassword@localhost:5433/postgres',
    echo = False 
)

print('db engine is created')