from app.blueprints.transports import bp
from app.extensions import auth
from apiflask import HTTPError
from app.blueprints import role_required
from app.blueprints.transports.schemas import (
    TransportResponseSchema,
    TransportUpdateSchema, 
    TransportAssignSchema,
    TransportCreateSchema,
    
)
from app.blueprints.transports.service import TransportService


# Összes szállítás listázása 
@bp.get('/')
@bp.auth_required(auth)
@role_required(["Admin", "Transport", "Warehouse"])
@bp.output(TransportResponseSchema(many=True))
def transport_list_all():
    return TransportService.list_transports()



# Egy konkrét szállítás lekérdezése 
@bp.get('/<int:transport_id>')
@bp.auth_required(auth)
@role_required(["Admin", "Transport"])
@bp.output(TransportResponseSchema)
def transport_get_by_id(transport_id):
    current_user_id = auth.current_user.get("user_id")
    current_roles = [r["name"] for r in auth.current_user.get("roles", [])]

    transport = TransportService.get_transport_by_id(transport_id, current_user_id, current_roles)
    if not transport:
        raise HTTPError(status_code=404, message="Transport not found or unauthorized")
    return transport


# Szállítás státuszának frissítése 
@bp.patch('/<int:transport_id>')
@bp.auth_required(auth)
@role_required(["Transport", "Admin"])
@bp.input(TransportUpdateSchema, location="json")
@bp.output(TransportResponseSchema)
def transport_update_status(transport_id, json_data):
    current_user_id = auth.current_user.get("user_id")
    current_roles = [r["name"] for r in auth.current_user.get("roles", [])]

    updated = TransportService.update_transport_status(
        transport_id,
        new_status=json_data["status"],
        current_user_id=current_user_id,
        roles=current_roles,
        load_date=json_data.get("load_date")  
    )

    if not updated:
        raise HTTPError(status_code=404, message="Transport not found or unauthorized")
    return updated


@bp.put('/<int:transport_id>/assign')
@bp.auth_required(auth)
@role_required(["Transport", "Admin"])
@bp.input(TransportAssignSchema, location="json")
@bp.output(TransportResponseSchema)
def transport_assign_vehicle(transport_id, json_data):  
    updated = TransportService.assign_vehicle(transport_id, json_data)
    if not updated:
        raise HTTPError(status_code=404, message="Hozzárendelés sikertelen vagy nem található")
    return updated

# új fuvar hozzáadása
@bp.post('/')
@bp.auth_required(auth)
@role_required(["Transport", "Admin"])
@bp.input(TransportCreateSchema, location="json")  
@bp.output(TransportResponseSchema, status_code=201)
def create_transport_order(json_data):
    created = TransportService.create_new_transport_order(json_data)
    if not created:
        raise HTTPError(400, message="Fuvarfeladat létrehozása sikertelen")
    return created