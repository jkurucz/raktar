from marshmallow import Schema, fields
from apiflask.fields import Integer, Boolean, DateTime

class OrderItemSchema(Schema):
    product_id = Integer()
    quantity = Integer()

class OrderCreateSchema(Schema):
    items = fields.List(fields.Nested(OrderItemSchema))

class OrderStatusSchema(Schema):
    status = fields.String()
    status_date = fields.DateTime()

class OrderResponseSchema(Schema):
    id = Integer()
    order_date = DateTime()
    closed = Boolean()
    status = fields.Nested(OrderStatusSchema, many=True)