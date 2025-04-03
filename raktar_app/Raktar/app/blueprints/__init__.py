from apiflask import APIBlueprint

bp = APIBlueprint('main', __name__, tag="default")

@bp.route('/')
def index():
    return 'This is The Main Blueprint'

from app.blueprints.user import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')

from app.blueprints.orders import bp as bp_order
bp.register_blueprint(bp_order, url_prefix='/order')


from app.blueprints.suppliers import bp as bp_supplyer
bp.register_blueprint(bp_supplyer, url_prefix='/supplier')

from app.blueprints.transports import bp as bp_transport
bp.register_blueprint(bp_transport, url_prefix='/transport')

from app.blueprints.warehouse import bp as bp_warehouse
bp.register_blueprint(bp_warehouse, url_prefix='/warehouse')


from app.models import *