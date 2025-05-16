from flask import jsonify, request
from app.blueprints import role_required
from app.blueprints.user import bp
from app.blueprints.user.schemas import (
    UserResponseSchema,
    UserRequestSchema,
    UserLoginSchema,
    RoleSchema,
    AddressSchema,
    ChangePasswordSchema,
    UserUpdateWithoutPasswordSchema
)
from app.blueprints.user.service import UserService
from apiflask import HTTPError
from app.extensions import auth


@bp.post('/users/register')
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def register_user(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/users/login')
@bp.input(UserLoginSchema, location="json")
@bp.output(UserResponseSchema)
def login_user(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/users/me')
@bp.output(UserResponseSchema)
@bp.auth_required(auth)
@role_required(["Admin"])
def get_my_profile():
    user_id = auth.current_user.get("user_id")
    success, response = UserService.get_user_by_id(user_id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=404)


@bp.put('/users/me')
#@bp.input(UserRequestSchema(partial=True))
@bp.input(UserUpdateWithoutPasswordSchema, location="json")
@bp.output(UserResponseSchema)
@bp.auth_required(auth)
@role_required(["Admin", "User", "Warehouse", "Supplier", "Transport"])
def update_my_profile(json_data):
    user_id = auth.current_user.get("user_id")
    success, response = UserService.update_user(user_id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put('/users/me/password')
@bp.input(ChangePasswordSchema)
@bp.auth_required(auth)
def change_password(json_data):
    user_id = auth.current_user.get("user_id")
    success, response = UserService.change_user_password(user_id, json_data)
    if success:
        return {"message": "Password updated successfully"}, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/users/me/roles')
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["User"])
def get_my_roles():
    user_id = auth.current_user.get("user_id")
    success, response = UserService.list_user_roles(user_id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/roles')
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
def get_roles():
    success, response = UserService.user_list_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/users/me/addresses')
@bp.input(AddressSchema, location="json")
@bp.auth_required(auth)
def add_my_address(json_data):
    user_id = auth.current_user.get("user_id")
    success, response = UserService.user_add_address(user_id, json_data)
    if success:
        return {"address_id": response}, 200
    raise HTTPError(message=response, status_code=400)

# Összes felhasználó
@bp.get('/')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.output(UserResponseSchema(many=True))
def list_users():
    users = UserService.get_all_users()
    
    if users:
        return users, 200
    raise HTTPError(message="No users found", status_code=400)



@bp.get('/users/<int:user_id>')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.output(UserResponseSchema)
def get_user_by_id(user_id):
    success, response = UserService.get_user_by_id(user_id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=404)

# Felhasználó módosítása jelszó nélkül:
@bp.put('/users/<int:user_id>/safe-update')
@bp.auth_required(auth)
@role_required(["Admin"])
@bp.input(UserUpdateWithoutPasswordSchema, location="json")
@bp.output(UserResponseSchema)
def safe_update_user(user_id, json_data):
    success, response = UserService.safe_update_user(user_id, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

