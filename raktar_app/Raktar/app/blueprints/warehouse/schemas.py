from marshmallow import Schema, fields
from apiflask.fields import Integer, String, DateTime


# ✅ Készlet frissítéshez (input)
class StockUpdateSchema(Schema):
    product_id = Integer(required=True)
    warehouse_id = Integer(required=True)
    quantity = Integer(required=True)


# ✅ Készlet válaszhoz (output)
class WarehouseStockSchema(Schema):
    id = Integer()
    product_id = Integer()
    warehouse_id = Integer()
    quantity = Integer()
    last_updated = DateTime()


# ✅ Fuvar hozzárendeléshez (input)
class TransportAssignSchema(Schema):
    order_id = Integer(required=True)
    carrier_id = Integer(required=True)
    transport_id = Integer(required=False)  # opcionális, ha előre definiált szállítóeszköz van


# ✅ Fuvar visszaadásához (output)
class TransportOrderSchema(Schema):
    id = Integer()
    order_id = Integer()
    carrier_id = Integer()
    transport_id = Integer()
    load_date = DateTime()
