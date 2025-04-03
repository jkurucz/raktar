from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus
from sqlalchemy import select
from datetime import datetime

class OrderService:
    @staticmethod
    def create_order(user_id, data):
        order = Order(user_id=user_id, order_date=datetime.utcnow(), closed=False)
        db.session.add(order)
        db.session.flush()
        for item in data['items']:
            db.session.add(OrderItem(order_id=order.id, **item))
        db.session.commit()
        return order

    @staticmethod
    def list_user_orders(user_id):
        return db.session.scalars(select(Order).filter_by(user_id=user_id)).all()
