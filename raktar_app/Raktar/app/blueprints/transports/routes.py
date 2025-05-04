from app.blueprints.transports import bp
from app.extensions import auth
from apiflask import HTTPError
from app.blueprints import role_required
from app.blueprints.transports.schemas import (
    TransportResponseSchema,
    TransportUpdateSchema
)
from app.blueprints.transports.service import TransportService


# 🔎 Összes szállítás listázása – csak Admin vagy LogisticsManager
@bp.get('/')
@bp.auth_required(auth)
@role_required(["Administrator", "LogisticsManager"])
@bp.output(TransportResponseSchema(many=True))
def transport_list_all():
    return TransportService.list_transports()



# 🔍 Egy konkrét szállítás lekérdezése – Admin vagy érintett Carrier
@bp.get('/<int:transport_id>')
@bp.auth_required(auth)
@role_required(["Administrator", "Carrier"])
@bp.output(TransportResponseSchema)
def transport_get_by_id(transport_id):
    current_user_id = auth.current_user.get("user_id")
    current_roles = [r["name"] for r in auth.current_user.get("roles", [])]

    transport = TransportService.get_transport_by_id(transport_id, current_user_id, current_roles)
    if not transport:
        raise HTTPError(status_code=404, message="Transport not found or unauthorized")
    return transport


# ✏️ Szállítás státuszának frissítése – csak Carrier (saját fuvar) vagy Admin
@bp.patch('/<int:transport_id>')
@bp.auth_required(auth)
@role_required(["Carrier", "Administrator"])
@bp.input(TransportUpdateSchema, location="json")
@bp.output(TransportResponseSchema)
def transport_update_status(transport_id, json_data):
    current_user_id = auth.current_user.get("user_id")
    current_roles = [r["name"] for r in auth.current_user.get("roles", [])]

    updated = TransportService.update_transport_status(
        transport_id,
        json_data["status"],
        current_user_id,
        current_roles
    )

    if not updated:
        raise HTTPError(status_code=404, message="Transport not found or unauthorized")
    return updated
