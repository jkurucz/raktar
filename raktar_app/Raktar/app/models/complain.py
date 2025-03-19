from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text, TIMESTAMP
from sqlalchemy import ForeignKey
from datetime import datetime

class Complaint(db.Model):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    order: Mapped["Order"] = relationship(back_populates="complaints")
    user: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"Complaint(id={self.id!r}, order_id={self.order_id!r}, user_id={self.user_id!r})"

