from app.blueprints.transports import bp
from app.blueprints.transports.schemas import TransportResponseSchema, TransportUpdateSchema
from app.blueprints.transports.service import TransportService
from apiflask import HTTPError

@bp.get('/')
@bp.output(TransportResponseSchema(many=True))
def list_transports():
    return TransportService.list_transports()

@bp.patch('/<int:tid>')
@bp.input(TransportUpdateSchema, location="json")
@bp.output(TransportResponseSchema)
def update_transport(tid, json_data):
    updated = TransportService.update_transport_status(tid, json_data["status"])
    if not updated:
        raise HTTPError(status_code=404, message="Transport not found")
    return updated