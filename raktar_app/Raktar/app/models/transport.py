from __future__ import annotations

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.extensions import db


class Transport(db.Model):
    __tablename__ = "transports"

    id: Mapped[int] = mapped_column(primary_key=True)
    truck: Mapped[str] = mapped_column(String(50), nullable=False)
    company: Mapped[str] = mapped_column(String(100), nullable=False)

    transport_orders: Mapped[List["TransportOrder"]] = relationship(back_populates="transport", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Transport(id={self.id!r}, truck={self.truck!s}, company={self.company!s})"
