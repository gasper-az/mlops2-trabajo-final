from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from wine_graphql_api.schema import schema

graphql_router = GraphQLRouter(schema)

app = FastAPI(title="Wine inference GraphQL", version="1.0.0")
app.include_router(graphql_router, prefix="/graphql")


@app.get("/health")
def health():
    return {"status": "ok"}
