from ariadne import QueryType
from engine import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, Post

query = QueryType()
# 在schema.py中定义了session dependency所以可以用orm操作
@query.field('hello')
def hello(*_):
    return 'Hello world'

@query.field('user')
async def resolve_user(_, info, id):
    session = info.context.get('session')
    user = await session.get(User, int(id))
    return user


@query.field('users')
async def resolve_users(_, info):
    session = info.context.get('session')
    users = await session.execute(select(User))
    return users.scalars().all()

@query.field('post')
async def resolve_post(_, info, id):
    session = info.context.get('session')
    post = await session.get(Post, int(id))
    return post

@query.field('posts')
async def resolve_posts(_, info):
    session = info.context.get('session')
    users = await session.execute(select(Post))
    return users.scalars().all()