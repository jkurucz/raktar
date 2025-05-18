from flask import request
from app.blueprints.products import bp
from app.extensions import auth
from apiflask import HTTPError
from app.blueprints import role_required
from app.blueprints.products.schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema
)
from app.blueprints.products.service import ProductService


# Termékek listázása + keresés (?search=...)
@bp.get('/')
@bp.auth_required(auth)
@role_required(["Admin", "User", "Warehouse", "Transport", "Supplier"])
@bp.output(ProductResponseSchema(many=True))
def list_products():
    search_term = request.args.get("search")
    return ProductService.get_all_products(search_term)


# Egy termék lekérdezése ID alapján
@bp.get('/<int:product_id>')
@bp.output(ProductResponseSchema)
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if product:
        return product
    raise HTTPError(status_code=404, message="Product not found")


# ➕ Új termék létrehozása
@bp.post('/')
@bp.auth_required(auth)
@role_required(["Admin", "Warehouse", "Supplier"])
@bp.input(ProductCreateSchema, location="json")
@bp.output(ProductResponseSchema)
def create_product(json_data):
    success, result = ProductService.create_product(json_data)
    if success:
        return result
    raise HTTPError(message=result, status_code=400)

# Termék módosítása
@bp.put('/<int:product_id>/')
@bp.auth_required(auth)
@role_required(["Admin", "Warehouse", "Supplier"])
@bp.input(ProductUpdateSchema, location="json")
@bp.output(ProductResponseSchema)
def update_product(product_id, json_data):
    success, result = ProductService.update_product(product_id, json_data)
    if success:
        return result
    raise HTTPError(message=result, status_code=404)


# Termék törlése
@bp.delete('/<int:product_id>')
@bp.auth_required(auth)
@role_required(["Admin", "Warehouse"])
def delete_product(product_id):
    success = ProductService.delete_product(product_id)
    if success:
        return {"message": "Product deleted"}
    raise HTTPError(message="Product not found", status_code=404)
