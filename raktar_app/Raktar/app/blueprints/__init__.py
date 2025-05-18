from functools import wraps
from apiflask import APIBlueprint
from app.extensions import auth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'],
        )
        if data["exp"] < int(datetime.now().timestamp()):
            return None
        return data
    except Exception as ex:
        return None

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            user_roles = [item["name"] for item in auth.current_user.get("roles")]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)
            raise HTTPError(message="Access denied", status_code=403)

        return decorated_function
    return wrapper

bp = APIBlueprint('main', __name__, tag="default")

from app.blueprints.user import bp as bp_user
bp.register_blueprint(bp_user, url_prefix='/user')

from app.blueprints.orders import bp as bp_order
bp.register_blueprint(bp_order, url_prefix='/order')

from app.blueprints.products import bp as bp_product
bp.register_blueprint(bp_product, url_prefix='/product')

from app.blueprints.complaints import bp as bp_complaint
bp.register_blueprint(bp_complaint, url_prefix='/complaint')

from app.blueprints.suppliers import bp as bp_supplyer
bp.register_blueprint(bp_supplyer, url_prefix='/supplier')

from app.blueprints.transports import bp as bp_transport
bp.register_blueprint(bp_transport, url_prefix='/transport')

from app.blueprints.transcomp import bp as bp_transcomp
bp.register_blueprint(bp_transcomp, url_prefix='/transcomp')

from app.blueprints.warehouse import bp as bp_warehouse
bp.register_blueprint(bp_warehouse, url_prefix='/warehouse')

from app.models import *