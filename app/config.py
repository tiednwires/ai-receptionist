"""Application configuration loaded from defaults and environment variables."""

# lru_cache lets us create the settings object once and reuse it throughout
# the application instead of rereading the environment on every request.
from functools import lru_cache

# BaseSettings reads configuration values from environment variables.
# SettingsConfigDict controls how Pydantic locates and handles those values.
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Define the configuration values available to the application."""

    # These defaults are used when matching environment variables are absent.
    # Pydantic can override them with APP_NAME and ENVIRONMENT values.
    app_name: str = "AI Receptionist"
    environment: str = "development"

    # Also look for configuration values in a local .env file.
    # Unknown values are ignored so adding an unrelated environment variable
    # does not prevent the application from starting.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return the application's shared, validated settings object."""

    # The first call creates Settings. Later calls return the cached instance.
    return Settings()
