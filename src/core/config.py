from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    bot_token: str = Field(description="Токен Telegram бота от @BotFather")
    database_url: str = Field(description="DSN для подключения к PostgreSQL")
    redis_url: str = Field(description="URL для подключения к Redis")
    owner_id: int = Field(description="Telegram ID владельца бота")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()