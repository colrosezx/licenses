import json
from pydantic import EmailStr, Field
from sqlalchemy import Result, Select
from core.models import database_helper as db_helper
from core.models import Customer
from sqlalchemy.orm import Session
from typing import Annotated, Dict, List, Optional



def create_customer(session: Session,
                    name: str,
                    TIN: Annotated[str, Field(..., min_length=12, max_length=12)],
                    email: EmailStr,
                    phone_number: Annotated[str, Field(..., min_length=11, max_length=11)],
                    contact_persons: str,
                    details: Optional[Dict] = None,
                    license_history: Optional[list] = None,
                    active_licenses: Optional[list] = None,
                    notes: Optional[str] = None 
                    ) -> Customer:
    customer = Customer(name=name,
                        TIN=TIN,
                        contact_persons=contact_persons,
                        email=email,
                        phone_number=phone_number,
                        details=details,
                        license_history=license_history,
                        active_licenses=active_licenses,
                        notes=notes)
    session.add(customer)
    session.commit()
    return customer

def update_customer(session: Session, id_customer: int) -> Customer:
    pass

def delete_customer_by_TIN(session: Session, TIN: str) -> None:
    stmt = Select(Customer).where(Customer.TIN == TIN)
    customer: Customer | None = session.scalar(stmt)
    if customer:
        print(f"{customer} deleted")
        session.delete(customer)
        session.commit()
    else:
        raise NameError("Not Found")

def read_customer_by_TIN(session: Session, TIN: str) -> Customer | None:
    stmt = Select(Customer).where(Customer.TIN == TIN)
    customer: Customer | None = session.scalar(stmt)
    if customer:
        return customer 
    else:
        raise NameError("Not Found")

def read_customers(session: Session) -> list[Customer]:
    stmt = Select(Customer).order_by(Customer.id)
    result: Result = session.execute(stmt)
    customers = result.scalars().all()

    return list(customers)


def main():
    # with db_helper.sessionmaker() as session:
    #     Gregory = create_customer(
    #         session=session,
    #         name="Gregory",
    #         TIN="987654321012",
    #         email="GregVladimidorich@gmail.com",
    #         phone_number="89745612301",
    #         contact_persons="Malcev Gregory Vladimirovich"            
    #     )

    #     print(Gregory)

    with db_helper.sessionmaker() as session:
        delete_customer_by_TIN(session=session,
                                     TIN="987654321012")


if __name__ == "__main__":
    main()