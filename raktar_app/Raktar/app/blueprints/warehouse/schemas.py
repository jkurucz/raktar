from marshmallow import Schema, fields
from apiflask.fields import Integer, String, DateTime



class StockUpdateSchema(Schema):
    product_id = Integer(required=True)
    warehouse_id = Integer(required=True)
    quantity = Integer(required=True)



class WarehouseStockSchema(Schema):
    id = Integer()
    product_id = Integer()
    warehouse_id = Integer()
    quantity = Integer()
    last_updated = DateTime()
    product_name = fields.String(dump_only=True)
    warehouse_location = fields.String(dump_only=True)


class TransportAssignSchema(Schema):
    order_id = Integer(required=True)
    carrier_id = Integer(required=True)
    transport_id = Integer(required=False)  


class TransportOrderSchema(Schema):
    id = Integer()
    order_id = Integer()
    carrier_id = Integer()
    transport_id = Integer()
    load_date = DateTime()

class WarehouseSchema(Schema):
    id = Integer()
    storage_location = String()
