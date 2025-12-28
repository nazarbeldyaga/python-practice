from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # FastAPI налаштування
    PROJECT_NAME: str = "Monad Transaction Scanner"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Блокчейн налаштування
    # Якщо змінної немає в .env, буде помилка (валидація як у NestJS)
    RPC_WS_URL: str = Field(..., alias="RPC_WS_URL")

    # База даних
    POSTGRES_URL: str = Field(..., alias="DATABASE_URL")

    # Автоматично зчитуємо з .env файлу
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# Створюємо єдиний екземпляр налаштувань (Singleton)
settings = Settings()