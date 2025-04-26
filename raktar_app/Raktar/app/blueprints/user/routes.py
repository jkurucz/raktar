from flask import jsonify
from app.blueprints import role_required
from app.blueprints.user import bp
from app.blueprints.user.schemas import UserResponseSchema, UserRequestSchema, UserLoginSchema, RoleSchema, AddressSchema
from app.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Email, Nested, Integer, List
from app.extensions import auth

@bp.route('/')
def index():
    return 'This is The User Blueprint'

@bp.post('/registrate')
@bp.doc(tags=["user"])
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def user_registrate(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

    

@bp.post('/login')
@bp.doc(tags=["user"])
@bp.input(UserLoginSchema, location="json")
@bp.output(UserResponseSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/roles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
def user_list_roles():
    success, response = UserService.user_list_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.get('/myroles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
#@role_required(["Admin", "Chef"]) #vesszővel elválasztva vagy kapcsolat
@role_required(["User"]) #Ellenőrzi, hogy nézheti e a tartalmat

def user_list_user_roles():
    success, response = UserService.list_user_roles(auth.current_user.get("user_id"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)





@bp.post('/address/add')
@bp.doc(tags=["user"])
@bp.input(AddressSchema, location="json")
def user_address_add(json_data):
    success, response = UserService.user_add_address(json_data)
    if success:
        return str(response), 200
    raise HTTPError(message=response, status_code=400)



