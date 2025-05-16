from app.extensions import db
from app.models.complain import Complaint
from app.models.order import Order
from sqlalchemy import select
from datetime import datetime

def add_user_name_to_complaints(complaints):
    for c in complaints:
        c.user_name = c.user.name if c.user else str(c.user_id)
        # order items: (csak ha van order reláció)
        if hasattr(c, "order") and c.order and hasattr(c.order, "items"):
            c.order_items = [
                {
                    "product_name": item.product.product_name if hasattr(item, "product") and item.product else f"#{item.product_id}",
                    "quantity": item.quantity
                }
                for item in c.order.items
            ]
        else:
            c.order_items = []
    return complaints

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
        complaints = db.session.scalars(
            select(Complaint).where(Complaint.user_id == user_id)
        ).all()
        return add_user_name_to_complaints(complaints)

    @staticmethod
    def list_all_complaints():
        """
        Összes panasz listázása (Admin számára).
        """
        complaints = db.session.scalars(
            select(Complaint)
        ).all()
        return add_user_name_to_complaints(complaints)

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
        return True, add_user_name_to_complaints(complaints)
