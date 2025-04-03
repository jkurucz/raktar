from app.blueprints.suppliers import bp
from app.blueprints.suppliers.schemas import SupplyFormSchema, SupplyResponseSchema
from app.blueprints.suppliers.service import SupplierService

@bp.post('/submit')
@bp.input(SupplyFormSchema, location="json")
@bp.output(SupplyResponseSchema)
def submit_supply(json_data):
    return SupplierService.submit_supply_form(json_data)