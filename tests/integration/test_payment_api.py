import pytest
from fastapi.testclient import TestClient

from api_tester.backend.app.main import app

client = TestClient(app)


@pytest.fixture
def mongo_clean():
    from api_tester.backend.app.db.mongo import db
    db.payments.delete_many({})
    yield
    db.payments.delete_many({})


def test_create_payment_api(mongo_clean):
    payload = {
        "booking_ref": "ABC123",
        "amount": 1500,
        "method": "card"
    }

    response = client.post("/api/payments/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["payment_id"].startswith("pay_")
    assert data["status"] == "pending"
    assert data["booking_ref"] == "ABC123"


def test_get_payment_api(mongo_clean):
    payload = {
        "booking_ref": "ABC123",
        "amount": 1500,
        "method": "card"
    }

    created = client.post("/api/payments/", json=payload).json()

    response = client.get(f"/api/payments/{created['payment_id']}")
    assert response.status_code == 200

    data = response.json()
    assert data["payment_id"] == created["payment_id"]


def test_cancel_payment_api(mongo_clean):
    payload = {
        "booking_ref": "ABC123",
        "amount": 1500,
        "method": "card"
    }

    created = client.post("/api/payments/", json=payload).json()

    response = client.delete(f"/api/payments/{created['payment_id']}")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "cancelled"


def test_payment_not_found(mongo_clean):
    response = client.get("/api/payments/pay_999999")
    assert response.status_code == 404
