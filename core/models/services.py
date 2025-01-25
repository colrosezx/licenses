from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .licenses import License
    from .objects import Object

class Service(Base):
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable="True")
    status: Mapped[str] = mapped_column(default="Неактивный", server_default="Неактивный")
    license_key: Mapped[str] = mapped_column(
        ForeignKey("licenses.license_key")
    )

    objects: Mapped[list["Object"]] = relationship(back_populates="service", cascade="all, delete-orphan")
    license: Mapped["License"] = relationship(back_populates="services", cascade="all, delete-orphan")