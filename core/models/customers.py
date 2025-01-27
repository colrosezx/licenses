from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON
from .base import Base
from typing import TYPE_CHECKING
    
if TYPE_CHECKING:
    from .objects import Object

class Customer(Base):  
    name: Mapped[str]
    TIN: Mapped[str]
    contact_persons: Mapped[list] = mapped_column(JSON, nullable=True)
    email: Mapped[str]
    phone_number: Mapped[str]
    status: Mapped[str] = mapped_column(default="Неактивный")
    count_of_licenses: Mapped[int] = mapped_column(default=0)
    details: Mapped[dict] = mapped_column(JSON, nullable=True)
    license_history: Mapped[list] = mapped_column(JSON, nullable=True)
    active_licenses: Mapped[list] = mapped_column(JSON, nullable=True)
    notes: Mapped[str] = mapped_column(nullable=True)

    objects: Mapped[list["Object"]] = relationship(back_populates="customer", 
                                                   foreign_keys="[Object.company_TIN]",
                                                   cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Customer(name={self.name}, email={self.email}, phone_number={self.phone_number})"

    def __str__(self):
        return f"Customer: {self.name}, Email: {self.email}, Phone: {self.phone_number}"

