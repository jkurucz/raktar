from __future__ import annotations
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime, Integer
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import List

class Supply(db.Model):
    __tablename__ = "supplies"

    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(nullable=False)
    delivery_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items: Mapped[List["SuppliedItem"]] = relationship(back_populates="supply", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Supply(id={self.id}, supplier_id={self.supplier_id}, delivery_date={self.delivery_date})>"
