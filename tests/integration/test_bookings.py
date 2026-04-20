from api_tester.backend.app.db.mongo import db


def test_single_booking_creation(auth_client):
    flight = db.flights.find_one({})
    assert flight is not None

    payload = {
        "flight_number": flight["flight_number"],
        "passenger": "Тест Тестов",
        "email": "test@example.com",
        "phone": "+79990001122",
        "has_luggage": True
    }

    response = auth_client.post("/api/bookings/", json=payload)
    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "confirmed"
    assert "booking_ref" in data
    assert "total_price" in data

    expected_price = flight["price"] + 500
    assert abs(data["total_price"] - expected_price) < 0.01

    updated = db.flights.find_one({"flight_number": flight["flight_number"]})
    assert updated["seats_available"] == flight["seats_available"] - 1

    booking = db.bookings.find_one({"booking_ref": data["booking_ref"]})
    assert booking is not None



def test_bulk_booking_creation(auth_client):
    flight = db.flights.find_one({})
    seats_before = flight["seats_available"]

    passengers = [
        {
            "name": "Иван Иванов",
            "email": "ivan@example.com",
            "phone": "+79990001111",
            "has_luggage": True,
            "seat_preference": "window"
        },
        {
            "name": "Пётр Петров",
            "email": "petr@example.com",
            "phone": "+79990002222",
            "has_luggage": False,
            "seat_preference": "aisle"
        }
    ]

    payload = {
        "flight_number": flight["flight_number"],
        "passengers": passengers,
        "promo_code": "SUMMER2024"
    }

    response = auth_client.post("/api/bookings/", json=payload)
    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["total_bookings_created"] == 2
    assert len(data["bookings"]) == 2

    expected_total = (flight["price"] + 500) + flight["price"]
    expected_discount = min(500, expected_total * 0.1)
    expected_after = expected_total - expected_discount

    assert abs(data["total_amount"] - expected_after) < 0.01
    assert abs(data["discount_applied"] - expected_discount) < 0.01

    updated = db.flights.find_one({"flight_number": flight["flight_number"]})
    assert updated["seats_available"] == seats_before - 2


def test_bulk_booking_not_enough_seats(auth_client):
    flight = db.flights.find_one({})
    seats_before = flight["seats_available"]

    passengers = [
        {
            "name": f"Пассажир {i}",
            "email": f"user{i}@example.com",
            "phone": f"+7999000{i:04d}",
            "has_luggage": False,
            "seat_preference": None
        }
        for i in range(seats_before + 3)
    ]

    payload = {
        "flight_number": flight["flight_number"],
        "passengers": passengers
    }

    response = auth_client.post("/api/bookings/", json=payload)
    assert response.status_code == 400

    data = response.json()
    assert "Недостаточно мест" in data["detail"]

    updated = db.flights.find_one({"flight_number": flight["flight_number"]})
    assert updated["seats_available"] == seats_before


def test_get_booking_by_ref(auth_client):
    flight = db.flights.find_one({})

    payload = {
        "flight_number": flight["flight_number"],
        "passenger": "Тест Получение",
        "email": "gettest@example.com",
        "phone": "+79990003344",
        "has_luggage": False
    }

    created = auth_client.post("/api/bookings/", json=payload).json()
    booking_ref = created["booking_ref"]

    response = auth_client.get(f"/api/bookings/{booking_ref}")
    assert response.status_code == 200

    data = response.json()
    assert data["booking_ref"] == booking_ref



def test_update_booking(auth_client):
    flight = db.flights.find_one({})

    created = auth_client.post("/api/bookings/", json={
        "flight_number": flight["flight_number"],
        "passenger": "Обновляемый Пассажир",
        "email": "update@example.com",
        "phone": "+79990004455",
        "has_luggage": False
    }).json()

    booking_ref = created["booking_ref"]

    update = auth_client.patch(f"/api/bookings/{booking_ref}", json={
        "email": "updated_email@example.com",
        "has_luggage": True
    })

    assert update.status_code == 200
    data = update.json()

    current = data["current_data"]
    assert current["email"] == "updated_email@example.com"
    assert current["has_luggage"] is True



def test_cancel_booking(auth_client):
    flight = db.flights.find_one({})
    seats_before = flight["seats_available"]

    created = auth_client.post("/api/bookings/", json={
        "flight_number": flight["flight_number"],
        "passenger": "Отменяемый Пассажир",
        "email": "cancel@example.com",
        "phone": "+79990005566",
        "has_luggage": False
    }).json()

    booking_ref = created["booking_ref"]

    response = auth_client.delete(f"/api/bookings/{booking_ref}")
    assert response.status_code == 200

    updated = db.flights.find_one({"flight_number": flight["flight_number"]})
    assert updated["seats_available"] == seats_before
