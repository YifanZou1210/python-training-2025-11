from fastapi import FastAPI
from schema import schema, get_context_value
from ariadne.asgi import GraphQL
"""
GraphQL Building Procedures
1. 写 GraphQL Schema SDL 
2. 为 schema 中的每个 type / field 编写 resolver
3. 组织所有 resolver 成 executable schema
4. 在 FastAPI 中挂载 GraphQL endpoint
5. 处理 context (session、dataloader、auth 等）
6. 优化(N+1、dataloader、loader batching)
"""
app = FastAPI()

app.mount('/graphql', GraphQL(schema, debug=True, context_value=get_context_value))


@app.get("/")
async def root():
    return {"message": "Hello World"}