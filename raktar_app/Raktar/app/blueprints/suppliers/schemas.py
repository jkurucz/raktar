from marshmallow import Schema, fields
from apiflask.fields import Integer, String, DateTime, List

class SuppliedItemSchema(Schema):
    product_id = Integer()
    quantity = Integer()

class SupplyFormSchema(Schema):
    supplier_id = Integer()
    delivery_date = DateTime()
    items = List(fields.Nested(SuppliedItemSchema))

class SupplyResponseSchema(Schema):
    supplier_id = Integer()
    delivery_date = DateTime()
    items = List(fields.Nested(SuppliedItemSchema))

