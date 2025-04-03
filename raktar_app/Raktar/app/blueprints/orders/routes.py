from app.blueprints.orders import bp
from app.blueprints.orders.schemas import OrderCreateSchema, OrderResponseSchema
from app.blueprints.orders.service import OrderService

@bp.post('/')
@bp.input(OrderCreateSchema, location="json")
@bp.output(OrderResponseSchema)
def create_order(json_data):
    user_id = 1 
    order = OrderService.create_order(user_id, json_data)
    return order

@bp.get('/')
@bp.output(OrderResponseSchema(many=True))
def list_orders():
    user_id = 1
    return OrderService.list_user_orders(user_id)
