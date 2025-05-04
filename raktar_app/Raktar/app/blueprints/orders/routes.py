from app.blueprints.orders import bp
from app.extensions import auth
from apiflask import HTTPError
from app.blueprints import role_required
from app.blueprints.orders.schemas import (
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderResponseSchema,
    OrderStatusSchema,
    OrderStatusCreateSchema
)
from app.blueprints.orders.service import OrderService


# Új rendelés létrehozása – bárki bejelentkezett felhasználó
@bp.post('/')
@bp.auth_required(auth)
@bp.input(OrderCreateSchema, location="json")
@bp.output(OrderResponseSchema)
def order_create(json_data):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.create_order(user_id, json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)


# Saját rendelések listázása
@bp.get('/')
@bp.auth_required(auth)
@bp.output(OrderResponseSchema(many=True))
def order_list_my():
    user_id = auth.current_user.get("user_id")
    return OrderService.list_user_orders(user_id)


# Egy rendelés lekérdezése (saját vagy admin)
@bp.get('/<int:order_id>')
@bp.auth_required(auth)
@bp.output(OrderResponseSchema)
def order_get_by_id(order_id):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.get_order(order_id, user_id)
    if success:
        return response
    raise HTTPError(message=response, status_code=404)


# ✏Rendelés módosítása (saját vagy admin)
@bp.put('/<int:order_id>')
@bp.auth_required(auth)
@bp.input(OrderUpdateSchema, location="json")
@bp.output(OrderResponseSchema)
def order_update(order_id, json_data):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.update_order(order_id, user_id, json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)


# Rendelés lezárása (saját vagy admin)
@bp.post('/<int:order_id>/close')
@bp.auth_required(auth)
def order_close(order_id):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.close_order(order_id, user_id)
    if success:
        return {"message": "Order closed successfully"}
    raise HTTPError(message=response, status_code=400)


# Státuszok lekérdezése – saját vagy admin
@bp.get('/<int:order_id>/statuses')
@bp.auth_required(auth)
@bp.output(OrderStatusSchema(many=True))
def order_list_statuses(order_id):
    user_id = auth.current_user.get("user_id")
    return OrderService.get_order_statuses(order_id, user_id)


# Új státusz hozzáadása – csak Admin vagy Chef
@bp.post('/<int:order_id>/statuses')
@bp.auth_required(auth)
@role_required(["Administrator", "Chef"])
@bp.input(OrderStatusCreateSchema, location="json")
@bp.output(OrderStatusSchema)
def order_add_status(order_id, json_data):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.add_order_status(order_id, user_id, json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)
