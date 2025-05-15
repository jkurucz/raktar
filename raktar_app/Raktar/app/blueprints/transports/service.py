from app.extensions import db
from app.models.transport_order import TransportOrder
from app.models.transport import Transport
from sqlalchemy import select
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload
from app.models.order import Order
from app.models.user import User
from app.models.order_item import OrderItem
from app.models.product import Product

class TransportService:

    @staticmethod
    def list_transports():
        transports = db.session.execute(
            select(TransportOrder)
            .options(
                joinedload(TransportOrder.order)
                .joinedload(Order.user)
                .joinedload(User.addresses),
                joinedload(TransportOrder.order)
                .joinedload(Order.items)
                .joinedload(OrderItem.product),
                joinedload(TransportOrder.transport)
            )
        ).unique().scalars().all()
    
        for t in transports:
            # Felhasználó neve
            t.user_name = t.order.user.name if t.order and t.order.user else "-"
    
            # Olvasható cím formázása
            t.user_address = (
                f"{addr.country}, {addr.postalcode} {addr.city}, {addr.street}"
                if (addr := t.order.user.addresses[0]) else "-"
            ) if t.order and t.order.user and t.order.user.addresses else "-"
    
            # Termékek neve és mennyisége
            t.items = [
                {
                    "product_name": item.product.product_name,
                    "quantity": item.quantity
                }
                for item in t.order.items if item.product
            ] if t.order and t.order.items else []
    
            # Fuvarozó cég és rendszám
            t.transport_company = t.transport.company if t.transport else None
            t.transport_truck = t.transport.truck if t.transport else None
    
        return transports

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
    def update_transport_status(transport_id, new_status, current_user_id=None, roles=None, load_date=None):
        """
        Szállítás státuszának frissítése, és opcionálisan a rakodási dátum beállítása.
        Carrier csak a saját fuvarját módosíthatja.
        """
        transport = db.session.get(TransportOrder, transport_id)
        if not transport:
            return None

        if roles and "Carrier" in roles and transport.carrier_id != current_user_id:
            return None  # jogosulatlan

        transport.status = new_status
        if load_date:
            transport.load_date = load_date

        transport.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return transport
    
    @staticmethod
    def assign_vehicle(transport_order_id, data):
        transport_order = db.session.get(TransportOrder, transport_order_id)
        if not transport_order:
            return None

        transport = db.session.get(Transport, data["transport_id"])
        if not transport:
            return None

        transport_order.transport = transport
        transport_order.status = data["status"]
        transport_order.load_date = data["load_date"]
        transport_order.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        return transport_order
