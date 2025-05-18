from app.blueprints.complaints import bp
from app.extensions import auth
from app.blueprints import role_required
from app.blueprints.complaints.schemas import (
    ComplaintCreateSchema,
    ComplaintResponseSchema
)
from app.blueprints.complaints.service import ComplaintService
from apiflask import HTTPError


# Új panasz beküldése – saját rendeléshez
@bp.post('/orders/<int:order_id>/complaints')
@bp.auth_required(auth)
@role_required(["Admin", "User"])
@bp.input(ComplaintCreateSchema, location="json")
@bp.output(ComplaintResponseSchema)
def complaint_create(order_id, json_data):
    user_id = auth.current_user.get("user_id")
    success, response = ComplaintService.create_complaint(order_id, user_id, json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)

# Összes panasz
@bp.get('/complaints')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.output(ComplaintResponseSchema(many=True))
def complaint_list_all():
    return ComplaintService.list_all_complaints()

# Saját panaszok lekérdezése
# @bp.get('/complaints')
# @bp.auth_required(auth)
# @role_required(["Admin"])
# @bp.output(ComplaintResponseSchema(many=True))
# def complaint_list_mine():
#     user_id = auth.current_user.get("user_id")
#     return ComplaintService.list_complaints(user_id)


# Adott rendelés panaszainak lekérdezése
@bp.get('/orders/<int:order_id>/complaints')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.output(ComplaintResponseSchema(many=True))
def complaint_list_order(order_id):
    user_id = auth.current_user.get("user_id")
    roles = [r["name"] for r in auth.current_user.get("roles", [])]
    success, response = ComplaintService.list_order_complaints(order_id, user_id, roles)
    if success:
        return response
    raise HTTPError(message=response, status_code=403)
