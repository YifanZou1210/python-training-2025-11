from ariadne import QueryType, MutationType, ObjectType
import httpx 
from .dataloader import UserTasksLoader
import asyncio 

REST_URL = "http://localhost:8000"

query = QueryType()
mutation = MutationType()
user_type = ObjectType('User')
task_type = ObjectType('Task')

@query.field('users')
async def resolve_users(_, info):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{REST_URL}/users",follow_redirects=True)
        if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/json"):
            users = r.json()
        else:
            users = []
    return users 
@query.field('user')
async def resolve_user(_, info, id):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{REST_URL}/users/{id}",follow_redirects=True)
        # 1. check status code == 200 here to avoid exception or return error messages 
        # 2. if user miss, return None 
        if r.status_code!=200:
            return None 
    return r.json()

@query.field('tasks')
async def resolve_tasks(_, info, userId = None, city = None):
    params = {} 
    if userId:
        params["user_id"] = userId
    if city:
        params["city"] = city 
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{REST_URL}/tasks/", params=params, follow_redirects=True)
        return r.json()

@query.field('task')
async def resolve_task(_, info, id):
    async with httpx.AsyncClient() as client:
        # para -> query parameters 
        r = await client.get(f"{REST_URL}/tasks/{id}",follow_redirects=True)
        if r.status_code!=200:
            return None 
        return r.json()
"""
mutation resolvers 
"""
@mutation.field("createUser")
async def resolve_create_user(_, info, name):
    jsons = {}
    if name:
        jsons["name"] = name 
    async with httpx.AsyncClient() as client:
        # json -> request body 
        r = await client.get(f"{REST_URL}/users/", json = jsons, follow_redirects=True)
        return r.json() 
    
@mutation.field('deleteUser')
async def resolve_delete_user(_, info, id):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{REST_URL}/users/{id}", follow_redirects=True)
        if r.status_code!=200:
            return None 
        return r.json()

@mutation.field('createTask')
async def resolve_create_task(_, info, title, content, city, userId):
    async with httpx.AsyncClient() as client:
        paylaod = {
            "title":title,
            "content":content,
            "city":city,
            "userId":userId
        }
        r = await client.get(f"{REST_URL}/tasks/", json = paylaod, follow_redirects=True)
        return r.json()
    
@mutation.field("updateTask")
async def resolve_update_task(_, info, id, title=None, content=None, city=None):
    async with httpx.AsyncClient() as client:
        payload = {}
        if title is not None: payload["title"] = title
        if content is not None: payload["content"] = content
        if city is not None: payload["city"] = city
        r = await client.put(f"{REST_URL}/tasks/{id}", json=payload, follow_redirects=True)
        if r.status_code != 200:
            return None
        return r.json()
    
@mutation.field("deleteTask")
async def resolve_delete_task(_, info, id):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{REST_URL}/tasks/{id}", follow_redirects=True)
        if r.status_code != 200:
            return None
        return r.json()

"""
Object Resolvers 
"""
@user_type.field('tasks')
async def resolve_user_tasks(obj, info):
    # from info.context to get context value, dic type 
    loader: UserTasksLoader = info.context["user_tasks_loader"]
    # Core methods of dataloader
    # 1. loader.load(key): push key into queue collection, recursively traversal dispatch and trigger batch_load_fn(keys)
    # 2. loader.load_many(keys): combined method of load() 
    return await loader.load(obj["id"])
    # obj: returned object from parent resolver
    # In this proj, obj -> parent -> User, child -> Tasks, means User.tasks 
    
    # Procedures of all resolvers, parent resolvers -> child resolvers -> subsequent ... 



    




