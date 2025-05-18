from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.extensions import db


class Address(db.Model):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(30), nullable=False)
    street: Mapped[str] = mapped_column(String(50), nullable=False)
    postalcode: Mapped[str] = mapped_column(String(10), nullable=False)

    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, country={self.country!r}, city={self.city!r}, street={self.street!r}, postalcode={self.postalcode!r})"
