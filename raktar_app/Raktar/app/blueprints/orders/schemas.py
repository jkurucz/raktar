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