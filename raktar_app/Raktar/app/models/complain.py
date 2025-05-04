from __future__ import annotations

import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text

from app.extensions import db


class Complaint(db.Model):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    order: Mapped["Order"] = relationship(back_populates="complaints")
    user: Mapped["User"] = relationship(back_populates="complaints")

    def __repr__(self) -> str:
        return f"Complaint(id={self.id!r}, order_id={self.order_id!r}, user_id={self.user_id!r})"
