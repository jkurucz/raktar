from app.extensions import db
from app.models.supply import Supply
from app.models.supplied_item import SuppliedItem
from sqlalchemy import select
from datetime import datetime


class SupplierService:

    @staticmethod
    def submit_supply_form(data: dict):
        try:
            supply = Supply(
                supplier_id=data["supplier_id"],
                delivery_date=data["delivery_date"]
            )

            for item in data["items"]:
                supplied_item = SuppliedItem(
                    product_id=item["product_id"],
                    quantity=item["quantity"]
                )
                supply.items.append(supplied_item)

            db.session.add(supply)
            db.session.commit()
            return True, supply

        except Exception as e:
            db.session.rollback()
            return False, f"Hiba beszállítás mentésekor: {str(e)}"

    @staticmethod
    def list_all_supplies():
        return db.session.scalars(select(Supply)).all()

    @staticmethod
    def get_supply_by_id(supply_id: int):
        return db.session.get(Supply, supply_id)

    @staticmethod
    def delete_supply(supply_id: int):
        supply = db.session.get(Supply, supply_id)
        if not supply:
            return False
        db.session.delete(supply)
        db.session.commit()
        return True
