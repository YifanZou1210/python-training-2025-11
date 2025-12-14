from ariadne import make_executable_schema, load_schema_from_path
from resolvers.query import query
from resolvers.mutations import mutation
from resolvers.type_resolvers import all_types
from engine import async_session_local, get_session
from aiodataloader import DataLoader
from dataloaders import batch_load_posts

type_def = load_schema_from_path('schema.graphql')
# 将type_def(graphql sdl), query resolvers, mutation resolvers, object-type field resolvers(all types) 组合成一个可执行的graphql schema
schema = make_executable_schema(
    type_def,
    [query, *all_types, mutation]
)

# GraphQL中每次请求都会调用一次get_context_value, 返回 shared info.context
async def get_context_value(request):
    # 1. 每个graphql请求创建一个独立的数据库session
    session = async_session_local()
    # session = await anext(get_session())
    print('session!!!', session)
    # 2. 提取客户端传的token, 之后可以对token decode
    token = request.headers.get('Authorization')
    print('token', token)
    # current_user = decode(token)
    return {
        "session": session,
        "request": request,
        # "current_user": current_user,
        # 防止n+1问题，自动避免
        "user_posts_loader": DataLoader(batch_load_posts)
    }
    