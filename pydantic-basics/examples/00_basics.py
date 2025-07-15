from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    """
    Represents a user in the system with type-validated fields.

    Attributes:
        id (UUID): A unique identifier for the user, auto-generated if not provided.
        name (str): Full name of the user.
        email (str): Email address of the user.
        dob (datetime): Date of birth (ISO 8601 format).
        metadata (dict[str, str]): Arbitrary metadata about the user (e.g., source, location).
        created_at (datetime): Timestamp when the user was created (UTC), set automatically.
        user_type (Literal): Role of the user. Must be one of "admin", "moderator", or "regular".
        is_active (bool): Whether the user account is active. Defaults to True.
    """

    id: UUID = Field(
        default_factory=uuid4,
        example="6c24581b-202c-4dc7-bf12-2bfa7d396f72",
        description="Unique user identifier (UUIDv4)",
    )
    name: str
    email: str
    dob: datetime = Field(
        example="1990-01-01T00:00:00Z",
        description="Date of birth (ISO 8601 timestamp)",
    )
    metadata: dict[str, str]
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the user was created (UTC)",
    )
    user_type: Literal["admin", "moderator", "regular"] = "regular"
    is_active: bool = True


def main() -> None:
    """
    Demonstrates how to create and serialize a User instance using Pydantic.
    """
    user = User(
        name="John Doe",
        email="john@doe.com",
        dob=datetime(1990, 1, 1),
        metadata={"source": "script", "location": "local"},
        user_type="admin",
    )

    # Serialize the User instance to a JSON string using Pydantic's `model_dump_json()`
    print(user.model_dump_json(indent=2))  # `indent=2` for pretty output


# Entry point guard to only execute when run directly
if __name__ == "__main__":
    main()
