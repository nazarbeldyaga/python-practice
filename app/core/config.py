from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "BSC Scanner"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    RPC_WS_URL: str = Field(..., alias="RPC_WS_URL")

    POSTGRES_URL: str = Field(..., alias="DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()