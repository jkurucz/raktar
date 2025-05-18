from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, TIMESTAMP

from app.extensions import db


class WarehouseStock(db.Model):
    __tablename__ = "warehouse_stocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    product: Mapped["Product"] = relationship(back_populates="warehouse_stocks")
    warehouse: Mapped["Warehouse"] = relationship(back_populates="warehouse_stocks")

    __table_args__ = (db.UniqueConstraint('product_id', 'warehouse_id', name='uq_product_warehouse'),)

    def __repr__(self) -> str:
        return f"WarehouseStock(id={self.id!r}, product_id={self.product_id!r}, quantity={self.quantity!r})"
