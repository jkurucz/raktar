from apiflask import APIBlueprint
bp = APIBlueprint('products', __name__, tag="products")
from app.blueprints.products import routes