from core.models import Service
from core.models import database_helper as db_helper
from sqlalchemy.orm import Session

def add_service(session: Session,
                name: str,
                description: str) -> Service:
    service = Service(
        name=name,
        description=description
    )
    session.add(service)
    session.commit()

    return service


def main():
    with db_helper.sessionmaker() as session:
        add_service(
            session=session,
            name="Service4",
            description="Description for service4"
        )

if __name__ == "__main__":
    main()

    