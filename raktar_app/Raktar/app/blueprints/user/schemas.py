# from marshmallow import Schema, fields
# from apiflask.validators import Length, Email

# class RoleSchema(Schema):
#     id = fields.Integer(dump_only=True)
#     name = fields.String(required=True)

# class AddressSchema(Schema):
#     country = fields.String(required=True, validate=Length(min=2))
#     city = fields.String(required=True)
#     street = fields.String(required=True)
#     postalcode = fields.String(required=True, validate=Length(min=3, max=10))

# class UserRequestSchema(Schema):
#     name = fields.String(required=True)
#     email = fields.Email(required=True)
#     password = fields.String(required=True, validate=Length(min=6))
#     phone = fields.String(required=True)
#     address = fields.Nested(AddressSchema, allow_none=True, required=False)

# class UserLoginSchema(Schema):
#     email = fields.Email(required=True)
#     password = fields.String(required=True)

# class UserResponseSchema(Schema):
#     id = fields.Integer()
#     name = fields.String()
#     email = fields.String()
#     phone = fields.String()
#     addresses = fields.List(fields.Nested(AddressSchema), allow_none=True)
#     roles = fields.List(fields.Nested(RoleSchema))
#     token = fields.String()

# class PayloadSchema(Schema):
#     user_id = fields.Integer()
#     roles = fields.List(fields.Nested(RoleSchema))
#     exp = fields.Integer()

# class ChangePasswordSchema(Schema):
#     current_password = fields.String(required=True, validate=Length(min=6))
#     new_password = fields.String(required=True, validate=Length(min=6))

# #jelszó nélküli userUpdate:
# class UserUpdateWithoutPasswordSchema(Schema):
#     name = fields.String(required=False)
#     email = fields.Email(required=False)
#     phone = fields.String(required=False)
#     address = fields.Nested(AddressSchema, allow_none=True, required=False)
#     roles = fields.List(fields.String(), required=False)

from marshmallow import Schema, fields
from apiflask.validators import Length, Email

class RoleSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

class AddressSchema(Schema):
    country = fields.String(required=True, validate=Length(min=2))
    city = fields.String(required=True)
    street = fields.String(required=True)
    postalcode = fields.String(required=True, validate=Length(min=3, max=10))

class UserRequestSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=6))
    phone = fields.String(required=True)
    address = fields.Nested(AddressSchema, allow_none=True, required=False)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    phone = fields.String()
    addresses = fields.List(fields.Nested(AddressSchema), allow_none=True)
    roles = fields.List(fields.Nested(RoleSchema))
    token = fields.String()

class PayloadSchema(Schema):
    user_id = fields.Integer()
    roles = fields.List(fields.Nested(RoleSchema))
    exp = fields.Integer()

class ChangePasswordSchema(Schema):
    current_password = fields.String(required=True, validate=Length(min=6))
    new_password = fields.String(required=True, validate=Length(min=6))

#jelszó nélküli userUpdate:
class UserUpdateWithoutPasswordSchema(Schema):
    name = fields.String(required=False)
    email = fields.Email(required=False)
    phone = fields.String(required=False)
    address = fields.Nested(AddressSchema, allow_none=True, required=False)
    roles = fields.List(fields.String(), required=False)