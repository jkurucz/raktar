from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import ForeignKey
from datetime import datetime

class TransportOrder(db.Model):
    __tablename__ = "transport_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    transport_id: Mapped[int] = mapped_column(ForeignKey("transports.id"), nullable=False)
    carrier_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)  # Fuvarozó ID
    load_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)  # "IN" vagy "OUT"

    order: Mapped["Order"] = relationship()
    transport: Mapped["Transport"] = relationship()
    carrier: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"TransportOrder(id={self.id!r}, order_id={self.order_id!r}, carrier_id={self.carrier_id!r})"
