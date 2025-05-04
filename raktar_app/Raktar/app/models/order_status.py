from __future__ import annotations

import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.extensions import db


class OrderStatus(db.Model):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    status_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    order: Mapped["Order"] = relationship(back_populates="statuses")

    def __repr__(self) -> str:
        return f"OrderStatus(id={self.id!r}, order_id={self.order_id!r}, status={self.status!s})"
