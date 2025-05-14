from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus
from app.models.product import Product
from sqlalchemy import select
from datetime import datetime


class OrderService:

    @staticmethod
    def create_order(user_id, data):
        order = Order(user_id=user_id, order_date=datetime.utcnow(), closed=False)
        db.session.add(order)
        db.session.flush()  # lekérjük az order.id-t

        for item in data['items']:
            db.session.add(OrderItem(order_id=order.id, **item))

        db.session.commit()
        return True, order

    @staticmethod
    def list_user_orders(user_id):
        return db.session.scalars(
            select(Order).where(Order.user_id == user_id)
        ).all()

    @staticmethod
    def get_order(order_id, user_id, roles=None):
        order = db.session.get(Order, order_id)
        if not order:
            return False, "Order not found"

        if order.user_id != user_id and "Administrator" not in (roles or []):
            return False, "Unauthorized to access this order"

        return True, order

    @staticmethod
    def update_order(order_id, user_id, data, roles=None):
        order = db.session.get(Order, order_id)
        if not order:
            return False, "Order not found"

        if order.user_id != user_id and "Administrator" not in (roles or []):
            return False, "Unauthorized to update this order"

        for key, value in data.items():
            setattr(order, key, value)

        db.session.commit()
        return True, order

    @staticmethod
    def close_order(order_id, user_id, roles=None):
        order = db.session.get(Order, order_id)
        if not order:
            return False, "Order not found"

        if order.user_id != user_id and "Administrator" not in (roles or []):
            return False, "Unauthorized to close this order"

        order.closed = True
        db.session.commit()
        return True, order

    @staticmethod
    def get_order_statuses(order_id, user_id, roles=None):
        order = db.session.get(Order, order_id)
        if not order:
            return []

        if order.user_id != user_id and "Administrator" not in (roles or []) and "Chef" not in (roles or []):
            return []

        return order.statuses

    @staticmethod
    def add_order_status(order_id, user_id, data, roles):
        if "Administrator" not in roles and "Chef" not in roles:
            return False, "Unauthorized to add order status"

        order = db.session.get(Order, order_id)
        if not order:
            return False, "Order not found"

        status = OrderStatus(
            order_id=order.id,
            status=data["status"],
            status_date=datetime.utcnow()
        )
        db.session.add(status)
        db.session.commit()
        return True, status
    
    @staticmethod
    def list_all_orders():
        return Order.query.all()
