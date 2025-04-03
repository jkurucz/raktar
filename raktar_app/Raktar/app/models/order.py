from __future__ import annotations

from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, TIMESTAMP
from sqlalchemy import ForeignKey
from typing import List
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    order_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    closed: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")
    statuses: Mapped[List["OrderStatus"]] = relationship(back_populates="order")
    complaints: Mapped[List["Complaint"]] = relationship(back_populates="order")


    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, user_id={self.user_id!r}, closed={self.closed!r})"

