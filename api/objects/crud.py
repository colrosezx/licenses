from datetime import date
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta
from ..settings.generate_key import random_key
from ..licenses.crud import create_license
from core.models import database_helper
from core.models import Object, Customer, Service, License

def create_object(session: Session,
                  name: str,
                  customer_TIN: str,
                  service_id: int,
                  description: Optional[str] = None) -> Object:
    
    license_for_object_creation = create_license(
            session=session,
            license_key=random_key,
            start_date=date.today(),
            end_date=(date.today() + relativedelta(months=1)),
            service_id=service_id
        )


    customer_query = select(Customer).where(Customer.TIN == customer_TIN)
    customer = session.execute(customer_query).scalar_one_or_none()

    service_query = select(Service).where(Service.id == service_id)
    service = session.execute(service_query).scalar_one_or_none()

    if customer is None:
        raise ValueError(f"Customer with TIN {customer_TIN} not found")
    if service is None:
        raise ValueError(f"Service with ID {service_id} not found")


    object = Object(
        name=name,
        customer_TIN=customer.TIN,
        service_id=service.id,
        license_key=license_for_object_creation,
        description=description
    )

    session.add(object)
    session.commit()

    return object



def update_objects_license_status(session: Session):

    objects_query = select(Object) 
    objects = session.execute(objects_query).scalars().all()

    for object in objects:
        license_query = select(License).where(License.license_key == object.license_key)
        license = session.execute(license_query).scalar_one_or_none()

        if license is None:
            print(f"License with key {object.license_key} not found for object {object.name}")
            continue

        if license.end_date >= date.today():
            new_status = "Активная"
        else:
            new_status = "Неактивная"

        update_object_license_status_query = (update(Object)
                                              .where(Object.id == object.id)
                                              .values(status=new_status)
                                              )
        session.execute(update_object_license_status_query)
    session.commit()


def main():
    with database_helper.sessionmaker() as session:
        update_objects_license_status(session=session)

if __name__ == "__main__":
    main()

