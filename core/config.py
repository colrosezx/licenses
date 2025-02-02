from pydantic_settings import BaseSettings

class ProjectSettings(BaseSettings):
    db_url: str = "sqlite:///core/database.db"
    db_echo: bool = False
    SECRET_KEY: str = "Zhopa"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

project_settings = ProjectSettings()
