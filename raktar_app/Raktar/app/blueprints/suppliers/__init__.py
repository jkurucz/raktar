from apiflask import APIBlueprint
bp = APIBlueprint('suppliers', __name__, tag="suppliers")
from app.blueprints.suppliers import routes