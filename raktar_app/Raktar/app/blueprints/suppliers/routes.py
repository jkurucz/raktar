from app.blueprints.suppliers import bp
from app.extensions import auth
from apiflask import HTTPError
from app.blueprints import role_required
from app.blueprints.suppliers.schemas import (
    SupplyFormSchema,
    SupplyResponseSchema
)
from app.blueprints.suppliers.service import SupplierService


# Új beszállítás rögzítése
@bp.post('/supplies')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.input(SupplyFormSchema, location="json")
@bp.output(SupplyResponseSchema)
def supply_create(json_data):
    success, response = SupplierService.submit_supply_form(json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)


# Összes beszállítás listázása
@bp.get('/supplies')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.output(SupplyResponseSchema(many=True))
def supply_list_all():
    return SupplierService.list_all_supplies()


# Egy beszállítás lekérdezése
@bp.get('/supplies/<int:supply_id>')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.output(SupplyResponseSchema)
def supply_get_by_id(supply_id):
    supply = SupplierService.get_supply_by_id(supply_id)
    if supply:
        return supply
    raise HTTPError(message="Supply not found", status_code=404)


# Beszállítás törlése 
@bp.delete('/supplies/<int:supply_id>')
@bp.auth_required(auth)
@role_required(["Admin"])
def supply_delete(supply_id):
    success = SupplierService.delete_supply(supply_id)
    if success:
        return {"message": "Supply deleted successfully"}
    raise HTTPError(message="Supply not found", status_code=404)
