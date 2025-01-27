from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from .base import Base
from datetime import date

if TYPE_CHECKING:
    from .services import Service
    from .objects import Object

class License(Base):
    
    license_key: Mapped[str] = mapped_column(unique=True)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default="Активный", server_default="Активный")
    service_id: Mapped[str] = mapped_column(
        ForeignKey("services.id")
    )

    object: Mapped["Object"] = relationship(back_populates="license",
                                              cascade="all, delete-orphan")

    service: Mapped["Service"] = relationship(back_populates="licenses", cascade="all, delete-orphan", single_parent=True)