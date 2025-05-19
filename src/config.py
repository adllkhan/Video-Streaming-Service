from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    SERVER_HOST: str = "0.0.0.0"  # noqa: S104
    SERVER_PORT: int = 8000
    SERVER_RELOAD: bool = True
    SERVER_DEBUG: bool = True
    SERVER_CORS_ORIGINS: list[str] = ["*"]
    SERVER_CREDENTIALS: bool = True
    SERVER_METHODS: list[str] = ["*"]
    SERVER_HEADERS: list[str] = ["*"]
    DATABASE_URL: str = "database"
    DATABASE_NAME: str = "streaming"
    DATABASE_USER: str = "streaming"
    DATABASE_PASSWORD: str = "streaming"  # noqa: S105
