from app.extensions import db
from app.models.warehouse_stock import WarehouseStock
from app.models.transport_order import TransportOrder
from sqlalchemy import select
from datetime import datetime, timezone
from app.models.product import Product
from app.models.warehouse_stock import WarehouseStock

def add_extra_fields_to_stocks(stocks):
    for stock in stocks:
        stock.product_name = stock.product.product_name if stock.product else f"#{stock.product_id}"
        stock.warehouse_location = stock.warehouse.storage_location if stock.warehouse else f"#{stock.warehouse_id}"
    return stocks

class WarehouseService:

    @staticmethod
    def update_warehouse_stock(data):

        try:
            stmt = select(WarehouseStock).where(
                WarehouseStock.product_id == data["product_id"],
                WarehouseStock.warehouse_id == data["warehouse_id"]
            )
            stock = db.session.execute(stmt).scalar_one_or_none()

            if stock:

                if stock.quantity + data["quantity"] < 0:
                    return False, "A készlet nem lehet negatív!"
                stock.quantity += data["quantity"]
            else:
                
                if data["quantity"] < 0:
                    return False, "A készlet nem lehet negatív!"
                stock = WarehouseStock(
                    product_id=data["product_id"],
                    warehouse_id=data["warehouse_id"],
                    quantity=data["quantity"]
                )
                db.session.add(stock)

            db.session.commit()
            return True, stock
        except Exception:
            db.session.rollback()
            return False, "Failed to update warehouse stock"




    @staticmethod
    def get_warehouse_stock(warehouse_id):

        stocks = db.session.scalars(
            select(WarehouseStock).where(WarehouseStock.warehouse_id == warehouse_id)
        ).all()
        return add_extra_fields_to_stocks(stocks)

    @staticmethod
    def assign_transport(data):

        try:
            transport_order = TransportOrder(
                order_id=data["order_id"],
                carrier_id=data["carrier_id"],
                transport_id=data.get("transport_id"),  
                load_date=datetime.now(timezone.utc)
            )
            db.session.add(transport_order)
            db.session.commit()
            return True, transport_order
        except Exception:
            db.session.rollback()
            return False, "Failed to assign transport"