from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "llama3-8b-8192"
    OPENAI_API_BASE: str = "https://api.openai.com/v1"  # 기본값 추가
    TEMPERATURE: float = 0.7

    class Config:
        env_file = ".env"

settings = Settings()