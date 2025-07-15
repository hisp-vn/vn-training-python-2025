from fastapi import FastAPI
from pydantic import BaseModel

d = """
## Welcome to FastAPI Basics
A simple example of __FastAPI__
"""

app = FastAPI(
    title="FastAPI Basics",
    description=d,
    version="0.1.0",
    contact={
        "name": "John Doe",
        "email": "john.doe@example.com",
    },
)


class Response(BaseModel):
    message: str


@app.get(
    "/",
    response_model=Response,
    tags=["index"],
)
async def index() -> Response:
    return Response(message="Hello, World!")
