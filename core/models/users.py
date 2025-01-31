from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from pydantic import EmailStr

if TYPE_CHECKING:
    from .customers import Customer

class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    status: Mapped[str] = mapped_column(default="def_user")

    customer: Mapped["Customer"] = relationship(back_populates="user")