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
from sqlalchemy import select
from app.models.transport_order import TransportOrder
from app.models.order import Order
from app.extensions import db


# Új rendelés létrehozása – bárki bejelentkezett felhasználó
@bp.post('/')
@bp.auth_required(auth)
@role_required(["Admin", "User"])
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
@role_required(["Admin", "User"])
@bp.output(OrderResponseSchema(many=True))
def order_list_my():
    user_id = auth.current_user.get("user_id")
    return OrderService.list_user_orders(user_id)


# Egy rendelés lekérdezése
@bp.get('/<int:order_id>')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.output(OrderResponseSchema)
def order_get_by_id(order_id):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.get_order(order_id, user_id)
    if success:
        return response
    raise HTTPError(message=response, status_code=404)


# ✏Rendelés módosítása 
@bp.put('/<int:order_id>')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.input(OrderUpdateSchema, location="json")
@bp.output(OrderResponseSchema)
def order_update(order_id, json_data):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.update_order(order_id, user_id, json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)


# Rendelés lezárása 
@bp.post('/<int:order_id>/close')
@bp.auth_required(auth)
@role_required(["Admin"])
def order_close(order_id):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.close_order(order_id, user_id)
    if success:
        return {"message": "Order closed successfully"}
    raise HTTPError(message=response, status_code=400)


# Státuszok lekérdezése 
@bp.get('/<int:order_id>/statuses')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.output(OrderStatusSchema(many=True))
def order_list_statuses(order_id):
    user_id = auth.current_user.get("user_id")
    return OrderService.get_order_statuses(order_id, user_id)


# Új státusz hozzáadása 
@bp.post('/<int:order_id>/statuses')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.input(OrderStatusCreateSchema, location="json")
@bp.output(OrderStatusSchema)
def order_add_status(order_id, json_data):
    user_id = auth.current_user.get("user_id")
    success, response = OrderService.add_order_status(order_id, user_id, json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)


# Összes megredelés
@bp.get('/all')
@bp.auth_required(auth)
@role_required(["Admin", "Transport", "Warehouse"])
@bp.output(OrderResponseSchema(many=True))
def order_list_all():
    return OrderService.list_all_orders()


# szállítás amihez nincs hozzárendelve fuvarozó
@bp.get('/unassigned')
@bp.auth_required(auth)
@role_required(["Admin", "Transport", "Warehouse"])
@bp.output(OrderResponseSchema(many=True))
def get_unassigned_orders():
    subquery = select(TransportOrder.order_id).scalar_subquery()
    orders = db.session.scalars(
        select(Order).where(~Order.id.in_(subquery))
    ).all()
    return orders
