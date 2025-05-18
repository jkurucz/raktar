from apiflask import APIBlueprint
bp = APIBlueprint('transcomp', __name__, tag="transcomp")
from app.blueprints.transcomp import routes