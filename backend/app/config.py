from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    admin_username: str
    admin_password: str

    betfair_username: str = ""
    betfair_password: str = ""
    betfair_app_key: str = ""

    the_odds_api_key: str = ""

    database_url: str = "sqlite:///./oddtobelieve.db"
    odds_poll_interval_minutes: int = 60

    log_level: str = "INFO"

    @field_validator("secret_key")
    @classmethod
    def secret_key_must_be_set(cls, v: str) -> str:
        if not v.strip():
            raise ValueError(
                "SECRET_KEY must be set via environment variable — refusing to start with empty key"
            )
        return v

    @field_validator("admin_username")
    @classmethod
    def admin_username_must_be_set(cls, v: str) -> str:
        if not v.strip():
            raise ValueError(
                "ADMIN_USERNAME must be set via environment variable — refusing to start with empty username"
            )
        return v

    @field_validator("admin_password")
    @classmethod
    def admin_password_must_be_set(cls, v: str) -> str:
        if not v.strip():
            raise ValueError(
                "ADMIN_PASSWORD must be set via environment variable — refusing to start with empty password"
            )
        return v


settings = Settings()
