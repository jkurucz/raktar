from marshmallow import Schema, fields
from apiflask.fields import Integer, String, DateTime
from apiflask.validators import OneOf

class TransportUpdateSchema(Schema):
    status = String(
        required=True,
        validate=OneOf(["assigned", "in transit", "delivered", "cancelled"])
    )

class TransportResponseSchema(Schema):
    id = Integer()
    order_id = Integer()
    carrier_id = Integer()
    transport_id = Integer(allow_none=True)
    status = String()
    updated_at = DateTime()
    load_date = DateTime()
