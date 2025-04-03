from app.extensions import db
from app.models.complain import Complaint
from sqlalchemy import select
from datetime import datetime

class ComplaintService:
    @staticmethod
    def create_complaint(data):
        complaint = Complaint(
            order_id=data["order_id"],
            message=data["message"],
            created_at=datetime.utcnow()
        )
        db.session.add(complaint)
        db.session.commit()
        return complaint

    @staticmethod
    def list_complaints():
        return db.session.scalars(select(Complaint)).all()