from app.extensions import db
from app.models.transport_order import TransportOrder
from sqlalchemy import select
from datetime import datetime

class TransportService:
    @staticmethod
    def list_transports():
        return db.session.scalars(select(TransportOrder)).all()

    @staticmethod
    def update_transport_status(tid, new_status):
        transport = db.session.get(TransportOrder, tid)
        if not transport:
            return None
        transport.status = new_status
        transport.updated_at = datetime.utcnow()
        db.session.commit()
        return transport