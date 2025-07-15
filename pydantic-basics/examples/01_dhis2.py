from typing import List

import httpx
from pydantic import BaseModel, Field


class IdSchemaIn(BaseModel):
    id: str


class DataElementIn(IdSchemaIn):
    name: str
    groups: List[IdSchemaIn] = Field(alias="dataElementGroups")


class MetadataResponse(BaseModel):
    data_elements: List[DataElementIn] = Field(alias="dataElements")


def main() -> None:
    """
    Fetches metadata from DHIS2 API and parses the response into structured models.
    """
    # Make a GET request to the DHIS2 demo server with basic auth
    response = httpx.get(
        "https://play.im.dhis2.org/dev/api/dataElements",
        auth=("admin", "district"),
        params={"paging": False, "fields": "id,name,dataElementGroups[id]"},
    )

    # Parse the response using the alias-aware model
    parsed = MetadataResponse.model_validate(response.json())

    # Print the first data element (as object and JSON)
    print(parsed.data_elements[0])  # __repr__ output of the Pydantic model
    print(parsed.data_elements[0].model_dump_json(indent=2))  # Pretty JSON output


# Entry point guard
if __name__ == "__main__":
    main()
