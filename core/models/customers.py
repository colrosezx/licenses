from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Customer(Base):  
    Company_name: Mapped[str]
    TIN: Mapped[int]
    Сontact_person: Mapped[str]
    Email: Mapped[str]
    Phone_number: Mapped[str]

