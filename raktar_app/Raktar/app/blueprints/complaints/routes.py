from app.blueprints.complaints import bp
from app.blueprints.complaints.schemas import ComplaintCreateSchema, ComplaintResponseSchema
from app.blueprints.complaints.service import ComplaintService

@bp.post('/')
@bp.input(ComplaintCreateSchema, location="json")
@bp.output(ComplaintResponseSchema)
def create_complaint(json_data):
    return ComplaintService.create_complaint(json_data)

@bp.get('/')
@bp.output(ComplaintResponseSchema(many=True))
def list_complaints():
    return ComplaintService.list_complaints()
