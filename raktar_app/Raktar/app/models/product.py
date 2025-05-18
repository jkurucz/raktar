from __future__ import annotations

from typing import List

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Text

from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)


    warehouse_stocks: Mapped[List["WarehouseStock"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.product_name!s})"
