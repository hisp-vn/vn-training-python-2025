from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    """
    Represents a user with validation and computed age.

    Attributes:
        id (UUID): Unique identifier for the user, auto-generated.
        email (str): User's email address. Validated to contain "@".
        name (str): Full name. Must be at least 2 characters long.
        dob (datetime): Date of birth. Must be timezone-aware.
        created_at (datetime): When the user was created. Defaults to now (UTC).

    Properties:
        age (int): The user's age, computed from date of birth.
    """

    # Auto-generated UUID if not explicitly provided
    id: UUID = Field(default_factory=uuid4)

    # Email field with custom validator (basic version)
    # Replace with: email: EmailStr for built-in full validation
    email: str

    # Name must be at least 2 characters long
    name: str = Field(min_length=2)

    # Date of birth (must be timezone-aware when passed in)
    dob: datetime

    # Automatically set to the current UTC time at creation
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("email")
    @classmethod
    def email_must_have_at_sign(cls, v: str) -> str:
        """
        Basic email validation ensuring '@' is present.

        Note:
            This is intentionally simplistic. In production, prefer `EmailStr`.
        """
        if "@" not in v:
            raise ValueError("Invalid email: missing '@'")

        return v

    @property
    def age(self) -> int:
        """
        Computed property that calculates the user's age in years
        based on the difference between the current UTC time and `dob`.
        """
        today = datetime.now(UTC)
        return int((today - self.dob).days / 365.25)


def main() -> None:
    """
    Entry point that instantiates a `User` object,
    prints the model data, and displays the computed age.
    """
    user = User(
        name="Alice",
        email="alice@example.com",
        dob=datetime(2000, 6, 15, tzinfo=UTC),  # tz-aware input is important
    )

    # Show full object (id, email, name, etc.)
    print(user)

    # Show computed age property
    print(f"User age: {user.age} years")


# Guard to only run `main()` when executed directly
if __name__ == "__main__":
    main()
