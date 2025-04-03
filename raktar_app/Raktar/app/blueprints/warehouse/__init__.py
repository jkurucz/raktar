from apiflask import APIBlueprint
bp = APIBlueprint('warehouse', __name__, tag="warehouse")
from app.blueprints.warehouse import routes