from marshmallow import Schema, fields
from apiflask.fields import Integer, DateTime, List


class SuppliedItemSchema(Schema):
    id = Integer(dump_only=True)
    product_id = Integer(required=True)
    quantity = Integer(required=True)


class SupplyFormSchema(Schema):
    supplier_id = Integer(required=True)
    delivery_date = DateTime(required=True)
    items = List(fields.Nested(SuppliedItemSchema), required=True)


class SupplyResponseSchema(Schema):
    id = Integer()
    supplier_id = Integer()
    delivery_date = DateTime()
    items = List(fields.Nested(SuppliedItemSchema))
