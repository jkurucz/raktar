from app.extensions import db
from app.models.complain import Complaint
from app.models.order import Order
from sqlalchemy import select
from datetime import datetime


class ComplaintService:

    @staticmethod
    def create_complaint(order_id: int, user_id: int, data: dict):
        """
        Panasz létrehozása saját rendeléshez.
        """
        order = db.session.get(Order, order_id)
        if not order:
            return False, "Order not found"

        if order.user_id != user_id:
            return False, "Unauthorized to create complaint for this order"

        complaint = Complaint(
            order_id=order_id,
            user_id=user_id,
            message=data["message"],
            created_at=datetime.utcnow()
        )
        db.session.add(complaint)
        db.session.commit()
        return True, complaint

    @staticmethod
    def list_complaints(user_id: int):
        """
        Saját panaszok listázása.
        """
        return db.session.scalars(
            select(Complaint).where(Complaint.user_id == user_id)
        ).all()

    @staticmethod
    def list_order_complaints(order_id: int, user_id: int, roles: list):
        """
        Adott rendelés panaszainak lekérdezése.
        Csak a rendelés tulajdonosa vagy Admin láthatja.
        """
        order = db.session.get(Order, order_id)
        if not order:
            return False, "Order not found"

        if order.user_id != user_id and "Administrator" not in roles:
            return False, "Unauthorized to view complaints for this order"

        complaints = db.session.scalars(
            select(Complaint).where(Complaint.order_id == order_id)
        ).all()
        return True, complaints
