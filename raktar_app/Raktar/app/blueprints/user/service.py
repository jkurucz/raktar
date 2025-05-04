from app.extensions import db
from app.models.user import User
from app.models.address import Address
from app.models.role import Role
from app.blueprints.user.schemas import UserResponseSchema, RoleSchema, PayloadSchema
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from authlib.jose import jwt
from flask import current_app
from werkzeug.security import check_password_hash

class UserService:

    @staticmethod
    def user_registrate(data):
        try:
            # Ellenőrizzük, hogy van-e már ilyen e-mail
            if db.session.execute(select(User).filter_by(email=data["email"])).scalar_one_or_none():
                return False, "E-mail already exists!"

            # Létrehozzuk a címet és a felhasználót
            address_data = data.pop("address")
            address = Address(**address_data)
            user = User(**data)
            user.set_password(user.password)
            user.addresses = [address]

            # Hozzáadjuk az alap "User" szerepkört
            user.roles.append(
                db.session.execute(select(Role).filter_by(name="User")).scalar_one()
            )

            db.session.add(user)
            db.session.commit()

            return True, UserResponseSchema().dump(user)

        except Exception as ex:
            return False, "Incorrect user data!"

    @staticmethod
    def user_login(data):
        try:
            user = db.session.execute(select(User).filter_by(email=data["email"])).scalar_one()

            if not user.check_password(data["password"]):
                return False, "Incorrect email or password!"

            user_schema = UserResponseSchema().dump(user)
            user_schema["roles"] = RoleSchema(many=True).dump(user.roles)
            user_schema["token"] = UserService.token_generate(user)

            return True, user_schema

        except Exception as ex:
            return False, "Incorrect login data!"

    @staticmethod
    def list_user_roles(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            return False, "User not found!"
        return True, RoleSchema(many=True).dump(user.roles)

    @staticmethod
    def user_list_roles():
        roles = db.session.query(Role).all()
        return True, RoleSchema(many=True).dump(roles)

    @staticmethod
    def get_user_by_id(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            return False, "User not found!"
        return True, UserResponseSchema().dump(user)

    @staticmethod
    def update_user(user_id, update_data):
        try:
            user = db.session.get(User, user_id)
            if user is None:
                return False, "User not found!"

            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            db.session.commit()
            return True, UserResponseSchema().dump(user)

        except Exception as ex:
            return False, "Failed to update user!"

    @staticmethod
    def change_user_password(user_id, data):
        try:
            user = db.session.get(User, user_id)
            if user is None:
                return False, "User not found!"

            if not user.check_password(data["current_password"]):
                return False, "Current password is incorrect!"

            user.set_password(data["new_password"])
            db.session.commit()
            return True, "Password updated"

        except Exception as ex:
            return False, "Failed to update password!"

    @staticmethod
    def user_add_address(user_id, data):
        try:
            user = db.session.get(User, user_id)
            if user is None:
                return False, "User not found!"

            address = Address(**data)
            address.user = user
            db.session.add(address)
            db.session.commit()
            return True, address.id

        except Exception as ex:
            return False, "Incorrect address data!"

    @staticmethod
    def token_generate(user: User):
        payload = {
            "user_id": user.id,
            "roles": RoleSchema(many=True).dump(user.roles),
            "exp": int((datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp())
        }

        return jwt.encode(
            {"alg": "RS256"},
            payload,
            current_app.config["SECRET_KEY"]
        ).decode()
