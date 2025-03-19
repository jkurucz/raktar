from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, TIMESTAMP
from sqlalchemy import ForeignKey
from datetime import datetime

class WarehouseStock(db.Model):
    __tablename__ = "warehouse_stocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    product: Mapped["Product"] = relationship()
    warehouse: Mapped["Warehouse"] = relationship(back_populates="warehouse_stocks")

    def __repr__(self) -> str:
        return f"WarehouseStock(id={self.id!r}, product_id={self.product_id!r}, quantity={self.quantity!r})"

