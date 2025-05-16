from marshmallow import Schema, fields
from apiflask.fields import Integer, String, DateTime
from apiflask.validators import OneOf

class TransportUpdateSchema(Schema):
    status = String(
        required=True,
        validate=OneOf(["assigned", "in transit", "delivered", "cancelled"])
    )
    load_date = DateTime(allow_none=True)

class TransportItemSchema(Schema):
    product_name = fields.String()
    quantity = fields.Integer()

class TransportResponseSchema(Schema):
    id = Integer()
    order_id = Integer()
    carrier_id = Integer()
    transport_id = Integer(allow_none=True)
    status = String()
    updated_at = DateTime()
    load_date = DateTime()
    user_name = String()         # új
    user_address = String()      # új
    items = fields.List(fields.Nested(TransportItemSchema)) 
    transport_company = String(allow_none=True)
    transport_truck = String(allow_none=True)

class TransportAssignSchema(Schema):
    transport_id = Integer(required=True)
    status = String(required=True, validate=OneOf(["in transit", "assigned"]))
    load_date = DateTime(required=True)

class TransportCreateSchema(Schema):
    order_id = Integer(required=True)
    transport_id = Integer(required=True)
    load_date = DateTime(required=True)
    direction = String(required=True, validate=OneOf(["outbound", "inbound"]))
