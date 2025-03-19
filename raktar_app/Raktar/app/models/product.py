from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Integer, Text
from typing import List

class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.product_name!s})"

