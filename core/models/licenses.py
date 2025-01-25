from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base
from datetime import date

if TYPE_CHECKING:
    from .services import Service

class License(Base):
    license_key: Mapped[str] = mapped_column(unique=True)
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default="Активный", server_default="Активный")

    services: Mapped[list["Service"]] = relationship(back_populates="license", cascade="all, delete-orphan")