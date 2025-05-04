from app.extensions import db
from app.models.warehouse_stock import WarehouseStock
from app.models.transport_order import TransportOrder
from sqlalchemy import select
from datetime import datetime, timezone


class WarehouseService:

    @staticmethod
    def update_warehouse_stock(data):
        """
        Új készlet létrehozása vagy meglévő frissítése adott raktárban.
        """
        try:
            stmt = select(WarehouseStock).where(
                WarehouseStock.product_id == data["product_id"],
                WarehouseStock.warehouse_id == data["warehouse_id"]
            )
            stock = db.session.execute(stmt).scalar_one_or_none()

            if stock:
                stock.quantity += data["quantity"]
            else:
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
        """
        Lekéri az adott raktárhoz tartozó készletlistát.
        """
        return db.session.scalars(
            select(WarehouseStock).where(WarehouseStock.warehouse_id == warehouse_id)
        ).all()

    @staticmethod
    def assign_transport(data):
        """
        Új szállítási megbízás hozzárendelése rendeléshez.
        """
        try:
            transport_order = TransportOrder(
                order_id=data["order_id"],
                carrier_id=data["carrier_id"],
                transport_id=data.get("transport_id"),  # lehet None is
                load_date=datetime.now(timezone.utc)
            )
            db.session.add(transport_order)
            db.session.commit()
            return True, transport_order
        except Exception:
            db.session.rollback()
            return False, "Failed to assign transport"