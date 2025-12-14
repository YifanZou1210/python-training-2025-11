
from fastapi import FastAPI
from ariadne.asgi import GraphQL
from ariadne import load_schema_from_path, make_executable_schema
from .resolvers import query, mutation, user_type, task_type
from .dataloader import UserTasksLoader

type_defs = load_schema_from_path("graphql_rest/schema.graphql")
# create graphql schema 
schema = make_executable_schema(type_defs, [query, mutation, user_type, task_type])

app = FastAPI()

@app.on_event('startup')
async def startup_event():
    print("GraphQL server is running on port 8001")

async def get_context_value(request):
    # context value must be dic-type
    return {"user_tasks_loader": UserTasksLoader()} # create dataloader instance

# Below, each client graphql request will trigger context_value -> get_context_value()-> return context (contain UserTaskLoader() instance)

# UserTaskLoader valid in this request lifecycle, in lifecyle 
# 1. object_resolver trigger dataloader through user_id 
# 2. collect multiple user_id in requests, call batch_load_fn(keys) in batch 
# 3. return res to resolver 
# 4. close dataloader

# mount Graphql app on '/' path 
app.add_route("/", GraphQL(schema, context_value=get_context_value))

# GraphQL()be like FastAPI() 
# GraphQL(schema) converted SDL schema + py resolvers into GraphQL server 
# GraphQL(context_value) para create and support conext_value to resolver ( resolver use info.context to access)

# Register router
# 1. @app.get/route() 
# 2. app.add_route(path, endpoint, methods)
