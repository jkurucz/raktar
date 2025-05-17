from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus
from app.models.product import Product
from sqlalchemy import select
from datetime import datetime
from app.models.transport_order import TransportOrder

class OrderService:

    @staticmethod
    def create_order(user_id, data):
        order = Order(user_id=user_id, order_date=datetime.utcnow(), closed=False)
        db.session.add(order)
        db.session.flush()  

        for item in data['items']:
            db.session.add(OrderItem(order_id=order.id, **item))

        db.session.commit()
        return True, order

    @staticmethod
    def list_user_orders(user_id):
        orders = db.session.scalars(
            select(Order).where(Order.user_id == user_id)
        ).all()
    
        for order in orders:
            order.user_name = order.user.name if order.user else "-"
            order.user_phone = order.user.phone if order.user and hasattr(order.user, "phone") else "-"
            if order.user and order.user.addresses and len(order.user.addresses) > 0:
                addr = order.user.addresses[0]
                order.user_address = f"{addr.country}, {addr.postalcode} {addr.city}, {addr.street}"
            else:
                order.user_address = "-"
    
            tos = order.transport_orders.order_by(TransportOrder.load_date.desc()).all()
            transport_order = tos[0] if tos else None
    
            if transport_order:
                order.transport_company = getattr(transport_order.transport, "company", None)
                order.transport_truck = getattr(transport_order.transport, "truck", None)
                order.load_date = transport_order.load_date
            else:
                order.transport_company = None
                order.transport_truck = None
                order.load_date = None
    
        return orders

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
        orders = Order.query.all()
        for order in orders:
            order.user_name = order.user.name if order.user else "-"
            order.user_phone = order.user.phone if order.user and hasattr(order.user, "phone") else "-"
            if order.user and order.user.addresses and len(order.user.addresses) > 0:
                addr = order.user.addresses[0]
                order.user_address = f"{addr.country}, {addr.postalcode} {addr.city}, {addr.street}"
            else:
                order.user_address = "-"

            tos = order.transport_orders.order_by(TransportOrder.load_date.desc()).all()
            transport_order = tos[0] if tos else None

            if transport_order:
                order.transport_company = getattr(transport_order.transport, "company", None)
                order.transport_truck = getattr(transport_order.transport, "truck", None)
                order.load_date = transport_order.load_date
            else:
                order.transport_company = None
                order.transport_truck = None
                order.load_date = None

        return orders