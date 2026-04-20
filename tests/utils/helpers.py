# tests/utils/helpers.py
import pytest
from fastapi.testclient import TestClient
from api_tester.backend.app.main import app

@pytest.fixture
def auth_client():
    client = TestClient(app)

    # создаём тестового пользователя
    client.post("/api/auth/register", json={
        "username": "test",
        "password": "test123"
    })

    # логинимся
    resp = client.post("/api/auth/login", data={
        "username": "test",
        "password": "test123"
    })

    token = resp.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client


def make_single_booking_payload(flight_number: str):
    return {
        "flight_number": flight_number,
        "passenger": "Тест Тестов",
        "email": "test@example.com",
        "phone": "+79990001122",
        "has_luggage": True
    }


def make_bulk_passengers(count: int):
    passengers = []
    for i in range(count):
        passengers.append({
            "name": f"Пассажир {i}",
            "email": f"user{i}@example.com",
            "phone": f"+7999000{i:04d}",
            "has_luggage": bool(i % 2),
            "seat_preference": None
        })
    return passengers

def assert_json_list(response):
    """
    Проверяет, что ответ — это JSON-список.
    Возвращает сам список.
    """
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    return data
