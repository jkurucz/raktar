from marshmallow import Schema, fields
from apiflask.validators import Length
from apiflask.fields import Integer, Boolean, DateTime

# ========== ORDER ITEM ==========
class OrderItemSchema(Schema):
    product_id = Integer(required=True)
    quantity = Integer(required=True)

# ========== ORDER CREATE / UPDATE ==========
class OrderCreateSchema(Schema):
    items = fields.List(fields.Nested(OrderItemSchema), required=True)

class OrderUpdateSchema(Schema):
    items = fields.List(fields.Nested(OrderItemSchema), required=True)


# ========== ORDER STATUS ==========
class OrderStatusSchema(Schema):
    status = fields.String(required=True)
    status_date = fields.DateTime(required=True)

class OrderStatusCreateSchema(Schema):
    status = fields.String(required=True)

# ========== ORDER RESPONSE ==========
class OrderResponseSchema(Schema):
    id = Integer()
    order_date = DateTime()
    closed = Boolean()
    status = fields.List(fields.Nested(OrderStatusSchema))
    items = fields.List(fields.Nested(OrderItemSchema))
    user_name = fields.String(dump_only=True)
    user_address = fields.String(dump_only=True)
    user_phone = fields.String(dump_only=True)
    transport_company = fields.String(allow_none=True, dump_only=True)
    transport_truck = fields.String(allow_none=True, dump_only=True)
    load_date = fields.DateTime(allow_none=True, dump_only=True)