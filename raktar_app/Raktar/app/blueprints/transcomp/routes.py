from app.blueprints.transcomp import bp
from app.blueprints import role_required
from app.blueprints.transcomp.schemas import TransportSchema
from app.blueprints.transcomp.service import TransportService
from app.extensions import auth
from apiflask import HTTPError
from flask import request

@bp.get("/")
@bp.output(TransportSchema(many=True))
@bp.auth_required(auth)
@role_required(["Admin", "Transport"])
def get_all():
    return TransportService.list_all()

@bp.post('/')
@bp.auth_required(auth)
@role_required(["Admin", "Transport"])
@bp.input(TransportSchema, location='json')
@bp.output(TransportSchema)
def create(json_data):  # ✅ legyen json_data
    success, result = TransportService.create_transcomp(json_data)
    if success:
        return result
    raise HTTPError(message=result, status_code=400)

@bp.delete("/<int:trans_id>")
@bp.auth_required(auth)
@role_required(["Admin", "Transport"])
def delete(trans_id):
    success, response = TransportService.delete(trans_id)
    if success:
        return {"message": response}
    raise HTTPError(message=response, status_code=404)