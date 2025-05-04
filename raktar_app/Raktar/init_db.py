from __future__ import annotations

from app import db, create_app
from config import Config
from sqlalchemy import text
from datetime import datetime, timezone

app = create_app(config_class=Config)
app.app_context().push()

# --- 1. Szerepkörök ---
from app.models.role import Role

roles_to_create = ["Administrator", "Chef", "Courier", "User", "LogisticsManager"]
existing_roles = {r.name for r in db.session.query(Role).all()}

for role_name in roles_to_create:
    if role_name not in existing_roles:
        db.session.add(Role(name=role_name))
db.session.commit()

roles = {r.name: r for r in db.session.query(Role).all()}

# --- 2. Felhasználók + Címek ---
from app.models.user import User
from app.models.address import Address

users = [
    {
        "name": "Admin",
        "email": "admin@example.com",
        "password": "admin123",
        "phone": "1111",
        "role": "Administrator",
        "address": {"country": "HU", "city": "Budapest", "street": "Fő utca 1", "postalcode": "1000"}
    },
    {
        "name": "Courier",
        "email": "courier@example.com",
        "password": "courier123",
        "phone": "2222",
        "role": "Courier",
        "address": {"country": "HU", "city": "Debrecen", "street": "Kossuth tér 2", "postalcode": "4026"}
    },
    {
        "name": "User",
        "email": "user@example.com",
        "password": "user123",
        "phone": "3333",
        "role": "User",
        "address": {"country": "HU", "city": "Pécs", "street": "Rákóczi út 3", "postalcode": "7621"}
    },
    {
        "name": "Manager",
        "email": "logistics@example.com",
        "password": "manager123",
        "phone": "4444",
        "role": "LogisticsManager",
        "address": {"country": "HU", "city": "Győr", "street": "Baross út 4", "postalcode": "9021"}
    }
]

created_users = {}

for u in users:
    if not db.session.query(User).filter_by(email=u["email"]).first():
        user = User(name=u["name"], email=u["email"], phone=u["phone"])
        user.set_password(u["password"])
        user.address = Address(**u["address"])
        user.roles.append(roles[u["role"]])
        db.session.add(user)
        created_users[u["role"]] = user

db.session.commit()

# --- 3. Termékek ---
from app.models.product import Product

products = [
    Product(product_name="Fúró", description="Ipari fúrógép", price=19999.90),
    Product(product_name="Kompresszor", description="Olajmentes kompresszor", price=54990.00),
    Product(product_name="Csiszológép", description="Fa- és fémmunkához", price=12990.50),
]
db.session.add_all(products)
db.session.commit()

# --- 4. Raktár + készlet ---
from app.models.warehouse import Warehouse
from app.models.warehouse_stock import WarehouseStock

warehouse = Warehouse(storage_location="Budapest - Központi raktár")
db.session.add(warehouse)
db.session.flush()

stocks = [
    WarehouseStock(product_id=products[0].id, warehouse_id=warehouse.id, quantity=15),
    WarehouseStock(product_id=products[1].id, warehouse_id=warehouse.id, quantity=8),
    WarehouseStock(product_id=products[2].id, warehouse_id=warehouse.id, quantity=20),
]
db.session.add_all(stocks)
db.session.commit()

# --- 5. Rendelés, rendelési tétel, státusz ---
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_status import OrderStatus

order = Order(user_id=created_users["User"].id, order_date=datetime.now(timezone.utc), closed=False)
db.session.add(order)
db.session.flush()

order_item = OrderItem(order_id=order.id, product_id=products[0].id, quantity=2)
order_status = OrderStatus(order_id=order.id, status="Rögzítve")
db.session.add_all([order_item, order_status])
db.session.commit()

# --- 6. Szállítási jármű + megbízás ---
from app.models.transport import Transport
from app.models.transport_order import TransportOrder

transport = Transport(truck="ABC-123", company="Trans Kft.")
db.session.add(transport)
db.session.flush()

transport_order = TransportOrder(
    order_id=order.id,
    transport_id=transport.id,
    carrier_id=created_users["Courier"].id,
    load_date=datetime.now(timezone.utc),
    direction="outbound"
)
db.session.add(transport_order)
db.session.commit()

# --- 7. Panasz ---
from app.models.complain import Complaint

complaint = Complaint(order_id=order.id, user_id=created_users["User"].id, message="A csomag sérült volt")
db.session.add(complaint)
db.session.commit()

print("Adatbázis inicializálva.")