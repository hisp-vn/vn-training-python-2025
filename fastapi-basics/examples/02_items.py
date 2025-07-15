from typing import Dict
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

# ---- Pydantic Model ----


class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4, example="6c24581b-202c-4dc7-bf12-2bfa7d396f72")
    name: str = Field(..., example="Item #1")

    model_config = ConfigDict(extra="forbid")


# ---- In-memory Store ----

items: Dict[UUID, Item] = {}

# ---- FastAPI App with Full OpenAPI Metadata ----

app = FastAPI(
    title="Item CRUD API",
    version="1.0.0",
    description="Simple root-mounted CRUD API for a single `Item` model.",
    summary="Root-level CRUD example for a resource.",
    contact={
        "name": "Your Name",
        "url": "https://your-domain.com",
        "email": "you@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    terms_of_service="https://your-domain.com/terms/",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc UI
    openapi_url="/openapi.json",  # OpenAPI schema
    openapi_tags=[
        {
            "name": "Items",
            "description": "Operations for creating, reading, updating, and deleting items.",
        },
    ],
)

# ---- CRUD Routes ----


@app.get(
    "/",
    response_model=list[Item],
    summary="List all items",
    tags=["Items"],
)
async def list_items():
    """Return all items in the __store__."""
    return list(items.values())


@app.post(
    "/",
    response_model=Item,
    summary="Create a new item",
    status_code=201,
    tags=["Items"],
)
async def create_item(item: Item):
    """Create a new item and return it."""
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items[item.id] = item
    return item


@app.get(
    "/{item_id}",
    response_model=Item,
    summary="Get item by ID",
    tags=["Items"],
)
async def get_item(item_id: UUID):
    """Retrieve an item by its UUID."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.put(
    "/{item_id}",
    response_model=Item,
    summary="Update item by ID",
    tags=["Items"],
)
async def update_item(item_id: UUID, updated_item: Item):
    """Replace an item by its UUID."""
    if item_id != updated_item.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = updated_item
    return updated_item


@app.delete(
    "/{item_id}",
    status_code=204,
    summary="Delete item by ID",
    tags=["Items"],
)
async def delete_item(item_id: UUID):
    """Delete an item by its UUID."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
