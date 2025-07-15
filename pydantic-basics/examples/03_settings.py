"""
Application Settings Loader with Pydantic, .env, and YAML Support

This script demonstrates a structured way to manage application configuration using:
- `pydantic-settings` for type-safe settings from environment variables
- `.env` file loading via `python-dotenv`
- Optional YAML overrides via `settings.yml`
- Cached lazy-loading for performance

Usage:
    settings = load_settings()
    print(settings.postgres_url)

Environment Variables:
    Can be declared in a `.env` file or in the shell.
YAML Override:
    If `settings.yml` exists, its values override those loaded from the environment.
"""

import logging
from functools import lru_cache
from pathlib import Path

import dotenv
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# ---------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------
logger = logging.getLogger(__name__)

# Load environment variables from a `.env` file if available
if not dotenv.load_dotenv():
    logger.warning(".env file not found, falling back to default values and YAML.")


# ---------------------------------------------------------
# Settings Model
# ---------------------------------------------------------
class Settings(BaseSettings):
    """
    Pydantic-based configuration model for application settings.

    Attributes:
        config_file (str): Path to the YAML configuration file (default: "settings.yml").
        host (str): Web server host binding (default: "0.0.0.0").
        port (int): Web server port (default: 8000).
        postgres_host (str): Hostname of the PostgreSQL server (default: "pg").
        postgres_port (int): Port of the PostgreSQL server (default: 5432).
        postgres_user (str): PostgreSQL username (default: "pg").
        postgres_password (str): PostgreSQL password (default: "pg").
        postgres_db (str): PostgreSQL database name (default: "pg").
        debug (bool): Enables debug mode if True (default: False).
    """

    config_file: str = Field(default="settings.yml")

    # Server settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # PostgreSQL settings
    postgres_host: str = Field(default="pg")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="pg")
    postgres_password: str = Field(default="pg")
    postgres_db: str = Field(default="pg")

    debug: bool = Field(default=False)

    @property
    def postgres_url(self) -> str:
        """
        Constructs the PostgreSQL connection URL.

        Returns:
            str: SQLAlchemy-compatible PostgreSQL connection string.
        """
        return (
            f"postgresql+psycopg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    # Pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore unknown environment variables
        env_prefix="",  # No prefix required for env vars
    )


# ---------------------------------------------------------
# Settings Loader (with YAML merge)
# ---------------------------------------------------------
@lru_cache()
def load_settings() -> Settings:
    """
    Loads settings using the following priority:
    1. .env file (via pydantic-settings)
    2. Default values in Settings model
    3. Override with settings.yml if present

    Returns:
        Settings: An instance of the validated settings model.
    """
    settings = Settings()  # Load from .env and model defaults

    yaml_path = Path(settings.config_file)
    if yaml_path.exists():
        try:
            with yaml_path.open("r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f) or {}
                merged = settings.model_dump()  # Dump current config
                merged.update(yaml_data)  # Override with YAML values
                settings = Settings(**merged)  # Re-parse as new Settings instance
        except Exception as e:
            logger.error(f"Failed to load settings.yml: {e}")

    return settings


# ---------------------------------------------------------
# Example Usage (for demonstration)
# ---------------------------------------------------------
if __name__ == "__main__":
    settings = load_settings()

    print(f"✅ Using config file: {settings.config_file}")
    print(f"📦 Loaded settings:\n{settings.model_dump()}")
    print(f"🐘 PostgreSQL URL: {settings.postgres_url}")
