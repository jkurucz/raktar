from marshmallow import Schema, fields
from apiflask.fields import Integer, String, DateTime


class ComplaintCreateSchema(Schema):
    message = String(required=True)


class ComplaintResponseSchema(Schema):
    id = Integer()
    order_id = Integer()
    user_id = Integer()
    message = String()
    created_at = DateTime()
