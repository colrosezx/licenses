from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import Select
from core.models import database_helper as db_helper
from ..settings.generate_key import random_key
from core.models import License, Service, Object
from sqlalchemy.orm import Session, joinedload, selectinload


def create_license(session: Session,
                   license_key: str,
                   start_date: date,
                   end_date: date,
                   service_id: int,
                   ) -> License:
    service_query: Service | None = Select(Service).where(Service.id == service_id)
    service = session.execute(service_query).scalar_one_or_none()
    if service:
        license = License(
            license_key=license_key,
            start_date=start_date,
            end_date=end_date,
            service_id=service_id
        )
    else:
        raise NameError("Service not Found")
    
    session.add(license)
    session.commit()

    return license.license_key

def main():
    with db_helper.sessionmaker() as session:
        pass

if __name__ == "__main__":
    main()