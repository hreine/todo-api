import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from starlette.middleware.cors import CORSMiddleware
from .database import get_db
from .schema import Query, CreateTodo, UpdateTodo, DeleteTodo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)


#GraphQLApp(schema=Query, mutations=[CreateTodo, UpdateTodo, DeleteTodo])

app.add_route("/graphql", graphql_app)

@app.on_event("startup")
async def startup():
    await get_db.connect()

@app.on_event("shutdown")
async def shutdown():
    await get_db.disconnect()