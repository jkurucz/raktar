from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, TIMESTAMP

from app.extensions import db


class TransportOrder(db.Model):
    __tablename__ = "transport_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    transport_id: Mapped[int] = mapped_column(ForeignKey("transports.id", ondelete="CASCADE"), nullable=False)
    carrier_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    load_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), nullable=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    # order = relationship("Order", back_populates="transport_orders")
    order: Mapped["Order"] = relationship(back_populates="transport_orders")
    transport: Mapped["Transport"] = relationship(back_populates="transport_orders")
    carrier: Mapped["User"] = relationship()
