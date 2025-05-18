from marshmallow import Schema, fields
from apiflask.fields import Integer, String, Float

class ProductCreateSchema(Schema):
    product_name = String(required=True)
    description = String()
    price = Float(required=True)

class ProductUpdateSchema(Schema):
    product_name = String()
    description = String()
    price = Float()

class ProductResponseSchema(Schema):
    id = Integer()
    product_name = String()
    description = String()
    price = Float()
