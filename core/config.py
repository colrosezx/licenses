from pydantic_settings import BaseSettings

class ProjectSettings(BaseSettings):
    db_url: str = "sqlite:///core/database.db"
    db_echo: bool = False

    SECRET_KEY: str = "Zhopa"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    COOKIES_SESSION_ID_KEY: str = "web-app-session-id"

project_settings = ProjectSettings()
