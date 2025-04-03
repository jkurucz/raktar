from app.blueprints.warehouse import bp
from app.blueprints.warehouse.schemas import StockAssignSchema, DeliveryStatusSchema
from app.blueprints.warehouse.service import WarehouseService

@bp.post('/stock/assign')
@bp.input(StockAssignSchema, location="json")
def assign_stock(json_data):
    result = WarehouseService.assign_stock_location(
        product_id=json_data['product_id'],
        storage_location=json_data['storage_location']
    )
    return {"status": "ok", "location": result.location}

@bp.post('/delivery/assign')
@bp.input(DeliveryStatusSchema, location="json")
def assign_carrier(json_data):
    result = WarehouseService.assign_delivery_carrier(
        order_id=json_data['order_id'],
        carrier_id=json_data['carrier_id']
    )
    return {"status": "ok", "transport_id": result.id}