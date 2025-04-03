from marshmallow import Schema, fields
from apiflask.fields import Integer, String, DateTime

class TransportUpdateSchema(Schema):
    status = String()

class TransportResponseSchema(Schema):
    id = Integer()
    order_id = Integer()
    carrier_id = Integer()
    status = String()
    updated_at = DateTime()