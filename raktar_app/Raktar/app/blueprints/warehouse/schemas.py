from marshmallow import Schema, fields
from apiflask.fields import Integer, String, DateTime

class StockAssignSchema(Schema):
    product_id = Integer()
    storage_location = String()

class DeliveryStatusSchema(Schema):
    order_id = Integer()
    carrier_id = Integer()