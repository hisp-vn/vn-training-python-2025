"""
FastAPI Parameter Handling and Validation Examples

This script demonstrates various FastAPI features:
- Accessing raw query parameters and headers
- Declarative parsing with `Query`, `Header`, and `Depends`
- Using Pydantic models for request parameter grouping
- Handling list inputs, aliases, defaults, and value constraints
"""

from typing import Annotated, Dict, List, Optional, Union

from fastapi import Depends, FastAPI, Header, Query, Request
from pydantic import BaseModel, Field

app = FastAPI()

# ---------------------------------------------------------
# Basic Echo of Request Contents
# ---------------------------------------------------------


class EchoResponse(BaseModel):
    """
    Response model used to return all request query parameters and headers.
    """

    query: Dict[str, List[str]] = {}
    headers: Dict[str, str] = {}


@app.get("/", response_model=EchoResponse)
async def echo_all(request: Request) -> EchoResponse:
    """
    GET /
    Echoes all incoming query parameters and headers.

    Returns:
        EchoResponse: Query parameters as lists and headers as strings.
    """
    query_params: Dict[str, List[str]] = {}

    for key, value in request.query_params.multi_items():
        query_params.setdefault(key, []).append(value)

    return EchoResponse(query=query_params, headers=dict(request.headers))


# ---------------------------------------------------------
# Explicit Query Parameter Handling
# ---------------------------------------------------------


class InputRequest(BaseModel):
    """
    Not used directly in this example, but shows how you might structure body/query models.
    """

    a: str = Field(..., description="Parameter a")
    b: Optional[List[str]] = Field(default=None, description="Parameter b")


@app.get("/parameters")
async def pydantic_get_parameter(
    a: str = Query(..., description="Parameter a"),
    b: List[str] = Query(default_factory=list, description="Parameter b"),
) -> Dict[str, Union[str, List[str]]]:
    """
    GET /parameters?a=foo&b=bar&b=baz
    Demonstrates explicit query param handling with defaults and lists.
    """
    return {"a": a, "b": b}


@app.get("/query-list")
async def get_query_list(a: Annotated[List[str], Query()] = []):
    """
    GET /query-list?a=1&a=2
    Parses multiple `a` query parameters into a list.
    """
    return a


@app.get("/required-optional")
def required_optional(q: str, optional: Optional[int] = None):
    """
    GET /required-optional?q=test&optional=123
    Mix of required (`q`) and optional (`optional`) parameters.
    """
    return {"q": q, "optional": optional}


@app.get("/alias")
def alias_example(camel_case_param: str = Query(..., alias="camelCaseParam")):
    """
    GET /alias?camelCaseParam=value
    Demonstrates aliasing query parameter names to match camelCase.
    """
    return {"camel_case_param": camel_case_param}


# ---------------------------------------------------------
# Grouping Query Parameters with Pydantic
# ---------------------------------------------------------


class PaginationParams(BaseModel):
    """
    Common pagination parameters that can be reused.
    """

    page: int = 1
    size: int = 10


@app.get("/pagination")
def pagination(params: Annotated[PaginationParams, Depends()]):
    """
    GET /pagination?page=1&size=10
    Automatically parses pagination params using a Pydantic model.
    """
    return {"page": params.page, "size": params.size}


# ---------------------------------------------------------
# Lists, Ranges, Defaults, and Meta
# ---------------------------------------------------------


@app.get("/tags")
def get_tags(tags: List[str] = Query(default=[])):
    """
    GET /tags?tags=foo&tags=bar
    Demonstrates multi-value query lists.
    """
    return {"tags": tags}


@app.get("/range")
def ranged(x: Annotated[int, Query(ge=10, le=100)]):
    """
    GET /range?x=42
    Validates that `x` is between 10 and 100 (inclusive).
    """
    return {"x": x}


# ---------------------------------------------------------
# Custom Default Using Dependency
# ---------------------------------------------------------


def default_query():
    """
    Used as a dependency to inject a default value.
    """
    return "from_dependency"


@app.get("/custom-default")
def custom_default(q: str = Depends(default_query)):
    """
    GET /custom-default
    Demonstrates using a callable dependency as the default value.
    """
    return {"q": q}


@app.get("/meta")
def meta_example(
    q: str = Query(..., title="Query", description="A required query string"),
    limit: int = Query(10, ge=1, le=100, description="Limit number of results"),
):
    """
    GET /meta?q=foo&limit=10
    Adds metadata to query parameters for documentation and validation.
    """
    return {"q": q, "limit": limit}


# ---------------------------------------------------------
# Path + Query + Header Combined
# ---------------------------------------------------------


@app.get("/combo/{item_id}")
def combo(
    item_id: int,
    q: Optional[str] = None,
    x_token: Optional[str] = Header(None),
):
    """
    GET /combo/123?q=abc with optional X-Token header
    Demonstrates combining path, query, and header inputs.
    """
    return {"item_id": item_id, "q": q, "x_token": x_token}
