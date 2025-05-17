from app.blueprints.warehouse import bp
from app.extensions import auth
from apiflask import HTTPError
from app.blueprints import role_required
from app.blueprints.warehouse.schemas import (
    StockUpdateSchema,
    WarehouseStockSchema,
    TransportAssignSchema,
    TransportOrderSchema
)
from app.blueprints.warehouse.service import WarehouseService
from app.models.warehouse import Warehouse
from app.blueprints.warehouse.schemas import WarehouseSchema

# Raktárkészlet frissítése 
@bp.post('/warehouse-stocks')
@bp.auth_required(auth)
@role_required(["Admin", "User", "Warehouse", "Supplier"])
@bp.input(StockUpdateSchema, location="json")
@bp.output(WarehouseStockSchema)
def warehouse_update_stock(json_data):
    success, response = WarehouseService.update_warehouse_stock(json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)


# Raktárkészlet lekérdezése – Admin / LogisticsManager / Chef
@bp.get('/warehouse-stocks/<int:warehouse_id>')
@bp.auth_required(auth)
@role_required(["Admin", "Warehouse", "User", "Transport", "Supplier"])
@bp.output(WarehouseStockSchema(many=True))
def warehouse_list_stock(warehouse_id):
    return WarehouseService.get_warehouse_stock(warehouse_id)


# Szállítás hozzárendelés – csak Admin vagy LogisticsManager
@bp.post('/transport-orders')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.input(TransportAssignSchema, location="json")
@bp.output(TransportOrderSchema)
def warehouse_assign_transport(json_data):
    success, response = WarehouseService.assign_transport(json_data)
    if success:
        return response
    raise HTTPError(message=response, status_code=400)

# Új: Raktárak lekérdezése
@bp.get('/warehouses')
@bp.auth_required(auth)
@role_required(["Admin", "Warehouse", "Transport", "Supplier"])
@bp.output(WarehouseSchema(many=True))
def warehouse_list():
    return Warehouse.query.all()