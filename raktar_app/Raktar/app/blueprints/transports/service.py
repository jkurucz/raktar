from app.extensions import db
from app.models.transport_order import TransportOrder
from sqlalchemy import select
from datetime import datetime, timezone


class TransportService:

    @staticmethod
    def list_transports():
        """
        Az összes szállítás listázása – csak Admin vagy LogisticsManager.
        """
        return db.session.scalars(select(TransportOrder)).all()

    @staticmethod
    def get_transport_by_id(transport_id, current_user_id=None, roles=None):
        """
        Egy konkrét szállítás lekérdezése.
        Ha Carrier, csak a sajátját láthatja.
        """
        transport = db.session.get(TransportOrder, transport_id)
        if not transport:
            return None

        if roles and "Carrier" in roles and transport.carrier_id != current_user_id:
            return None  # jogosulatlan

        return transport

    @staticmethod
    def update_transport_status(transport_id, new_status, current_user_id=None, roles=None):
        """
        Szállítás státuszának frissítése.
        Carrier csak a saját fuvarját módosíthatja.
        """
        transport = db.session.get(TransportOrder, transport_id)
        if not transport:
            return None

        if roles and "Carrier" in roles and transport.carrier_id != current_user_id:
            return None  # jogosulatlan

        transport.status = new_status
        transport.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return transport
