from apiflask import APIBlueprint
bp = APIBlueprint('transports', __name__, tag="transports")
from app.blueprints.transports import routes