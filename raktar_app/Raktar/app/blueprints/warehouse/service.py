from app.extensions import db
from app.models.transport_order import TransportOrder
from datetime import datetime

class WarehouseService:
    @staticmethod
    def assign_stock_location(product_id, storage_location):
        # Tárolóhely kezelését itt most csak visszaadjuk, mintha mentve lenne
        return type('MockStock', (object,), {"product_id": product_id, "location": storage_location})()

    @staticmethod
    def assign_delivery_carrier(order_id, carrier_id):
        transport = TransportOrder(order_id=order_id, carrier_id=carrier_id, status="assigned", updated_at=datetime.utcnow())
        db.session.add(transport)
        db.session.commit()
        return transport
