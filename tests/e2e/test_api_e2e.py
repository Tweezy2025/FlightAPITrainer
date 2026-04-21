import time
import os
import requests
import pytest
pytest.skip("Skipping e2e tests for now", allow_module_level=True)



# ================================
#  ОТКЛЮЧАЕМ ВСЕ ПРОКСИ WINDOWS
# ================================
# WinINET/WinHTTP игнорируют env-переменные, поэтому requests.Session().trust_env = False
session = requests.Session()
session.trust_env = False  # <-- ключевая строка, отключающая системный прокси

def r_get(url, **kwargs):
    return session.get(url, **kwargs)

def r_post(url, **kwargs):
    return session.post(url, **kwargs)

def r_delete(url, **kwargs):
    return session.delete(url, **kwargs)

BASE = "http://127.0.0.1:8000"
print("BASE =", BASE, type(BASE))

def wait_for_backend(timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = r_get(f"{BASE}/docs")
            if r.status_code in (200, 401, 404):
                return True
        except Exception:
            pass
        time.sleep(0.5)
    raise RuntimeError("Backend did not start in time")


def get_auth_headers():
    """
    Регистрируем пользователя и получаем Bearer-токен.
    """
    # 1. Регистрируем пользователя
    r_post(f"{BASE}/api/auth/register", json={
        "username": "e2e_user",
        "password": "e2e_pass"
    })

    # 2. Логинимся
    resp = r_post(f"{BASE}/api/auth/login", data={
        "username": "e2e_user",
        "password": "e2e_pass"
    })

    assert resp.status_code == 200, f"Login failed: {resp.text}"

    token = resp.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_e2e_full_booking_flow():
    # 0. Ждём backend
    wait_for_backend()

    # 1. Получаем токен
    headers = get_auth_headers()

    # 2. Получаем список рейсов
    flights_resp = r_get(f"{BASE}/api/flights/", headers=headers)
    assert flights_resp.status_code == 200

    flights = flights_resp.json()
    assert isinstance(flights, list)
    assert len(flights) > 0

    flight_number = flights[0]["flight_number"]

    # 3. Создаём бронирование
    payload = {
        "flight_number": flight_number,
        "passenger": "E2E Test",
        "email": "e2e@example.com",
        "phone": "+79990001122",
        "has_luggage": True
    }

    create_resp = r_post(f"{BASE}/api/bookings/", json=payload, headers=headers)
    assert create_resp.status_code in (200, 201), create_resp.text

    created = create_resp.json()
    assert "booking_ref" in created
    booking_ref = created["booking_ref"]

    # 4. Получаем бронирование
    get_resp = r_get(f"{BASE}/api/bookings/{booking_ref}", headers=headers)
    assert get_resp.status_code == 200

    booking = get_resp.json()
    assert booking["booking_ref"] == booking_ref
    assert booking["email"] == "e2e@example.com"

    # 5. Отменяем бронирование
    cancel_resp = r_delete(f"{BASE}/api/bookings/{booking_ref}", headers=headers)
    assert cancel_resp.status_code == 200

    cancel_data = cancel_resp.json()
    assert cancel_data["success"] is True
    assert cancel_data["booking_ref"] == booking_ref

    # 6. Проверяем, что бронирование удалено
    get_deleted = r_get(f"{BASE}/api/bookings/{booking_ref}", headers=headers)
    assert get_deleted.status_code == 404
