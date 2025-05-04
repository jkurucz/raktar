from __future__ import annotations
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.supply import Supply
    from app.models.product import Product

class SuppliedItem(db.Model):
    __tablename__ = "supplied_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    supply_id: Mapped[int] = mapped_column(ForeignKey("supplies.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    supply: Mapped["Supply"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()

    def __repr__(self):
        return f"<SuppliedItem(product_id={self.product_id}, quantity={self.quantity})>"
