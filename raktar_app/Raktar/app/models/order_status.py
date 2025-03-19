from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, TIMESTAMP
from sqlalchemy import ForeignKey
from datetime import datetime

class OrderStatus(db.Model):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    status_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    order: Mapped["Order"] = relationship(back_populates="statuses")

    def __repr__(self) -> str:
        return f"OrderStatus(id={self.id!r}, order_id={self.order_id!r}, status={self.status!s})"

