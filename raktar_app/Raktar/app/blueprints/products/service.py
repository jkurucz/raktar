from app.extensions import db
from app.models.product import Product
from sqlalchemy import select, or_
from app.models.warehouse import Warehouse
from app.models.warehouse_stock import WarehouseStock

class ProductService:

    @staticmethod
    def get_all_products(search_term=None):
        stmt = select(Product)
        if search_term:
            search = f"%{search_term.lower()}%"
            stmt = stmt.where(
                or_(
                    Product.product_name.ilike(search),
                    Product.description.ilike(search)
                )
            )
        return db.session.scalars(stmt).all()

    @staticmethod
    def get_product_by_id(product_id: int):
        return db.session.get(Product, product_id)

    @staticmethod
    def create_product(data: dict):
        try:
            product = Product(**data)
            db.session.add(product)
            db.session.flush()   # hogy product.id már meglegyen!
            # Minden warehouse-hoz 0-s készlet
            warehouses = db.session.scalars(select(Warehouse)).all()
            for warehouse in warehouses:
                stock = WarehouseStock(
                    product_id=product.id,
                    warehouse_id=warehouse.id,
                    quantity=0
                )
                db.session.add(stock)
            db.session.commit()
            return True, product
        except Exception as e:
            db.session.rollback()
            return False, f"Error creating product: {str(e)}"

    @staticmethod
    def update_product(product_id: int, data: dict):
        product = db.session.get(Product, product_id)
        if not product:
            return False, "Product not found"

        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()
        return True, product

    @staticmethod
    def delete_product(product_id: int):
        product = db.session.get(Product, product_id)
        if not product:
            return False
        db.session.delete(product)
        db.session.commit()
        return True
