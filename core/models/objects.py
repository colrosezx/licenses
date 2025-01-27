from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .customers import Customer
    from .services import Service

class Object(Base):
    name: Mapped[str]
    adress: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="Неактивный", server_default="Неактивный")

    company_name: Mapped[str] = mapped_column(
        ForeignKey("customers.name")
    )

    company_TIN: Mapped[str] = mapped_column(
        ForeignKey("customers.TIN")
    )

    service_name: Mapped[int] = mapped_column(
        ForeignKey("services.name")
    )

    customer: Mapped["Customer"] = relationship(back_populates="objects", 
                                                foreign_keys=[company_TIN],
                                                )
    service: Mapped["Service"] = relationship(back_populates="objects", cascade="all, delete-orphan", single_parent=True)
    