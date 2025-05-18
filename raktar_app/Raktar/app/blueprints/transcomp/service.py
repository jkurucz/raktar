from app.extensions import db
from app.models.transport import Transport
from app.blueprints.transcomp.schemas import TransportSchema
from sqlalchemy import select

class TransportService:

    @staticmethod
    def list_all():
        return Transport.query.all()

    @staticmethod
    def create(data):
        try:
            new_trans = Transport(**data)
            db.session.add(new_trans)
            db.session.commit()
            return True, TransportSchema().dump(new_trans)
        except Exception as ex:
            return False, str(ex)

    @staticmethod
    def delete(trans_id):
        trans = db.session.get(Transport, trans_id)
        if not trans:
            return False, "Transport not found"
        db.session.delete(trans)
        db.session.commit()
        return True, "Deleted"
    
    @staticmethod
    def create_transcomp(data):
        try:
            transcomp = Transport(**data)
            db.session.add(transcomp)
            db.session.commit()
            return True, TransportSchema().dump(transcomp)
        except Exception as e:
            return False, str(e) 