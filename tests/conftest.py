import pytest
from fastapi.testclient import TestClient
from api_tester.backend.app.main import app
from api_tester.backend.app.db.mongo import db


@pytest.fixture
def auth_client():
    client = TestClient(app)

    # создаём пользователя
    client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpass"
    })

    # логинимся
    resp = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpass"
    })

    token = resp.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client


@pytest.fixture(autouse=True)
def clean_db():
    db.bookings.delete_many({})
    db.flights.delete_many({})
    db.airlines.delete_many({})

    db.flights.insert_one({
        "flight_number": "SU100",
        "airline": "Аэрофлот",
        "departure": "SVO",
        "arrival": "LED",
        "departure_time": "2024-12-25T10:30:00Z",
        "arrival_time": "2024-12-25T13:45:00Z",
        "price": 8500.0,
        "seats_available": 10
    })

    db.airlines.insert_many([
        {"name": "Аэрофлот", "code": "SU"},
        {"name": "S7 Airlines", "code": "S7"}
    ])

    yield
