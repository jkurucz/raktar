from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List

class Warehouse(db.Model):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True)
    storage_location: Mapped[str] = mapped_column(String(50), nullable=False)

    warehouse_stocks: Mapped[List["WarehouseStock"]] = relationship(back_populates="warehouse")

    def __repr__(self) -> str:
        return f"Warehouse(id={self.id!r}, location={self.storage_location!s})"

