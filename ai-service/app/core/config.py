from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):

    GOOGLE_API_KEY: str

    POSTGRES_USER: str = "myuser"
    POSTGRES_PASSWORD: str = "mypassword"
    POSTGRES_DB: str = "findb"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    TEMPERATURE: float = 0.7

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()