from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from app.database import SupabaseDB


class Receipt:

    def __init__(self, user_id, store_name, receipt_date, total_amount, category, upload_date=None):
        # self.id = id
        db = SupabaseDB()
        self.user_id = user_id
        self.store_name = store_name
        self.receipt_date = receipt_date
        self.total_amount = total_amount
        self.category = category
        self.currency = db.get_user_currency(user_id)
        self.upload_date = upload_date or datetime.utcnow()

    def to_dict(self):

        return {
            # "id": self.id,
            "user_id": self.user_id,
            "store_name": self.store_name,
            "total_amount": self.total_amount,
            "receipt_date": self.receipt_date,
            "category": self.category,
            "currency": self.currency,
            "upload_date": self.upload_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            # id=data.get("id"),
            user_id=data["user_id"],
            store_name=data["store_name"],
            total_amount=data["total_amount"],
            receipt_date=data["receipt_date"],
            category=data["category"],
            # currency=data["currency"],
            upload_date=datetime.fromisoformat(data["upload_date"]) if data.get("upload_date") else None
        )