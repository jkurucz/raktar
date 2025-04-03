from marshmallow import Schema, fields
from apiflask.fields import Integer, String

class ComplaintCreateSchema(Schema):
    order_id = Integer()
    message = String()

class ComplaintResponseSchema(Schema):
    id = Integer()
    order_id = Integer()
    message = String()
    created_at = fields.DateTime()