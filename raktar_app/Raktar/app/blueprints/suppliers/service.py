from app.extensions import db
from app.models.order_item import OrderItem 
from datetime import datetime

class SupplierService:
    @staticmethod
    def submit_supply_form(data):
        items = []
        for item in data['items']:
            items.append(OrderItem(product_id=item['product_id'], quantity=item['quantity']))
            db.session.add(items[-1])
        db.session.commit()
        return {
            "supplier_id": data['supplier_id'],
            "delivery_date": data['delivery_date'],
            "items": items
        }

