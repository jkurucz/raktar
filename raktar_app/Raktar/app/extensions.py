from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

from apiflask import HTTPTokenAuth
auth = HTTPTokenAuth()
