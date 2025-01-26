from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from core.config import project_settings


class Database_Helper():

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_engine(
            url=url,
            echo=echo
        )

        self.sessionmaker = sessionmaker(
            bind = self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
            
        )

    def get_scoped_session(self):
        session = scoped_session(self.session_factory)
        return session
    
    def session_dependence(self) -> Session: # type: ignore
        session = self.get_scoped_session()
        try:
            yield session

        finally:
            session.remove()


database_helper = Database_Helper(
    url = project_settings.db_url,
    echo=project_settings.db_echo
)



