from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # about project
    PROJECT_NAME: str = "FeliX prep"
    PROJECT_VERSION: str = "0.1"
    PROJECT_DESCRIPTION: str = "Svgs similarity"

    # backend general settings
    BACKEND_CORS_ORIGINS: list[str] = []
    ALLOWED_HOSTS: list[str] = ["*"]

    SVG_REPOSITORY_API_BASE_URL: str = "https://api.svgrepo.com"
    SVG_REPOSITORY_BASE_URL: str = "https://www.svgrepo.com"
    MONGO_URL: str = "mongodb://localhost:27017/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
