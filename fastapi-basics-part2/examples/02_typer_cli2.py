import os
from typing import List, Optional

import httpx
import typer
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

app = typer.Typer()


class DataElement(BaseModel):
    id: str
    name: str = Field(alias="displayName")


class DataElementsResponse(BaseModel):
    dataElements: List[DataElement]


@app.command()
def fetch_data(
    url: Optional[str] = typer.Argument(None, help="Base URL of the API"),
    username: Optional[str] = typer.Option(None, help="API username"),
    password: Optional[str] = typer.Option(None, help="API password"),
):
    """
    Fetch and print dataElements (id, displayName) from the API.
    Uses environment variables if available, otherwise prompts for missing values.
    """

    # Fallback to env vars if CLI args not given
    url = url or os.getenv("API_URL")
    username = username or os.getenv("API_USERNAME")
    password = password or os.getenv("API_PASSWORD")

    # Prompt only if missing
    if not username:
        username = typer.prompt("Username")
    if not password:
        password = typer.prompt("Password", hide_input=True)
    if not url:
        typer.echo("❌ Missing URL. Provide via argument or set API_URL in .env", err=True)
        raise typer.Exit(1)

    api_url = f"{url.rstrip('/')}/api/dataElements"

    try:
        response = httpx.get(api_url, auth=(username, password))
        response.raise_for_status()

        data = DataElementsResponse.model_validate(response.json())

        for element in data.dataElements:
            typer.echo(f"{element.id}: {element.name}")

    except httpx.HTTPStatusError as e:
        typer.echo(f"❌ HTTP error {e.response.status_code}: {e.response.text}", err=True)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)


if __name__ == "__main__":
    app()
