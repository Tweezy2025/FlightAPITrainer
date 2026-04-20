import pytest
import uuid
from fastapi.testclient import TestClient
from api_tester.backend.app.main import app
from api_tester.backend.app.db.mongo import db  # прямой импорт

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_test_users():
    # чистим всех тестовых юзеров перед каждым тестом
    db["users"].delete_many({"username": {"$regex": "^user_"}})


def test_register_random_user():
    username = f"user_{uuid.uuid4().hex[:8]}"
    payload = {"username": username, "password": "pass123"}
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["status"] == "registered"


def test_register_fixed_user_and_duplicate():
    payload = {"username": "user_fixed", "password": "pass123"}
    resp1 = client.post("/api/auth/register", json=payload)
    assert resp1.status_code == 200, resp1.text
    assert resp1.json()["status"] == "registered"

    resp2 = client.post("/api/auth/register", json=payload)
    assert resp2.status_code == 400, resp2.text
    assert resp2.json()["detail"] == "User already exists"


def test_login_success():
    username = f"user_{uuid.uuid4().hex[:8]}"
    payload = {"username": username, "password": "pass123"}
    client.post("/api/auth/register", json=payload)

    resp = client.post("/api/auth/login", data=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    username = f"user_{uuid.uuid4().hex[:8]}"
    payload = {"username": username, "password": "pass123"}
    client.post("/api/auth/register", json=payload)

    resp = client.post("/api/auth/login", data={"username": username, "password": "wrongpass"})
    assert resp.status_code == 400, resp.text
    assert resp.json()["detail"] == "Invalid username or password"
