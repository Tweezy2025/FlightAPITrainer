import pytest
from datetime import datetime

from api_tester.backend.app.services.payment_service import PaymentService
from api_tester.backend.app.models.payment import PaymentCreate


@pytest.fixture
def mongo_clean():
    from api_tester.backend.app.db.mongo import db
    db.payments.delete_many({})
    yield
    db.payments.delete_many({})


def test_create_payment(mongo_clean):
    data = PaymentCreate(
        booking_ref="ABC123",
        amount=1000,
        method="card"
    )

    payment = PaymentService.create_payment(data)

    assert payment.payment_id.startswith("pay_")
    assert payment.booking_ref == "ABC123"
    assert payment.amount == 1000
    assert payment.method == "card"
    assert payment.status == "pending"
    assert isinstance(payment.created_at, datetime)


def test_get_payment(mongo_clean):
    data = PaymentCreate(
        booking_ref="ABC123",
        amount=1000,
        method="card"
    )
    created = PaymentService.create_payment(data)

    fetched = PaymentService.get_payment(created.payment_id)

    assert fetched is not None
    assert fetched.payment_id == created.payment_id


def test_cancel_payment(mongo_clean):
    data = PaymentCreate(
        booking_ref="ABC123",
        amount=1000,
        method="card"
    )
    created = PaymentService.create_payment(data)

    cancelled = PaymentService.cancel_payment(created.payment_id)

    assert cancelled.status == "cancelled"
