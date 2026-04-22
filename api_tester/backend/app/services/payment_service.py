import uuid
from datetime import datetime

from ..models.payment import Payment, PaymentCreate
from ..db.mongo import db


class PaymentService:

    @staticmethod
    def create_payment(data: PaymentCreate) -> Payment:
        payment_id = f"pay_{uuid.uuid4().hex[:8]}"

        payment = Payment(
            payment_id=payment_id,
            booking_ref=data.booking_ref,
            amount=data.amount,
            method=data.method,
            status="pending",
            created_at=datetime.utcnow()
        )

        db.payments.insert_one(payment.model_dump())
        return payment

    @staticmethod
    def get_payment(payment_id: str) -> Payment | None:
        doc = db.payments.find_one({"payment_id": payment_id})
        if not doc:
            return None
        return Payment(**doc)

    @staticmethod
    def update_status(payment_id: str, status: str) -> Payment | None:
        doc = db.payments.find_one_and_update(
            {"payment_id": payment_id},
            {"$set": {"status": status}},
            return_document=True
        )
        if not doc:
            return None
        return Payment(**doc)

    @staticmethod
    def cancel_payment(payment_id: str) -> Payment | None:
        return PaymentService.update_status(payment_id, "cancelled")
