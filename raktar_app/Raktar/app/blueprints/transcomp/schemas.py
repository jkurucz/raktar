from marshmallow import Schema, fields
from apiflask.validators import Length

class TransportSchema(Schema):
    id = fields.Integer(dump_only=True)
    truck = fields.String(required=True, validate=Length(min=2))
    company = fields.String(required=True, validate=Length(min=2))
