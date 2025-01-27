from pydantic_settings import BaseSettings

class ProjectSettings(BaseSettings):
    db_url: str = "sqlite:///core/database.db"
    db_echo: bool = False

project_settings = ProjectSettings()
