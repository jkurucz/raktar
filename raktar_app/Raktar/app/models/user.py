from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import Base
from app.extensions import db

UserRole = Table(
    "userroles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)

    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    roles: Mapped[List["Role"]] = relationship(secondary=UserRole, back_populates="users")
    orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    complaints: Mapped[List["Complaint"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!s}, email={self.email!r})"

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
