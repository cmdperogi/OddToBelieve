from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    admin_username: str = "admin"
    admin_password: str = "changeme"

    betfair_username: str = ""
    betfair_password: str = ""
    betfair_app_key: str = ""

    the_odds_api_key: str = ""

    database_url: str = "sqlite:///./oddtobelieve.db"
    odds_poll_interval_minutes: int = 60


settings = Settings()
