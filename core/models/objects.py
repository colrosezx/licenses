from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .customers import Customer
    from .services import Service
    from .licenses import License

class Object(Base):
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="Неактивный", server_default="Неактивный")

    customer_TIN: Mapped[str] = mapped_column(
        ForeignKey("customers.TIN")
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id")
    )

    license_key: Mapped[str] = mapped_column(
        ForeignKey(
            "licenses.license_key"
        )
    )

    license: Mapped["License"] = relationship(back_populates="object",
                                              cascade="all, delete-orphan",
                                              single_parent=True)

    customer: Mapped["Customer"] = relationship(back_populates="objects", 
                                                foreign_keys=[customer_TIN],
                                                )
    service: Mapped["Service"] = relationship(back_populates="objects", cascade="all, delete-orphan", single_parent=True)


    def __repr__(self):
        return f"Object(name={self.name}, description={self.description}, license_key={self.license_key})"

    def __str__(self):
        return f"Object: {self.name}, description: {self.description}, license_key: {self.license_key}"
    