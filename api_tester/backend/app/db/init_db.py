# app/db/init_db.py
from datetime import datetime, timedelta
from bson import ObjectId

from api_tester.backend.app.db.mongo import db


def reset_collections():
    """
    Полная очистка коллекций.
    """
    db.airlines.drop()
    db.flights.drop()
    db.bookings.drop()


def seed_airlines():
    airlines = [
        {"name": "Аэрофлот", "code": "SU"},
        {"name": "S7 Airlines", "code": "S7"},
        {"name": "UTair", "code": "UT"},
        {"name": "Pobeda", "code": "DP"},
    ]

    db.airlines.insert_many(airlines)
    print(f"[OK] Добавлено авиакомпаний: {len(airlines)}")


def seed_flights():
    now = datetime.utcnow()

    flights = [
        {
            "flight_number": "SU100",
            "airline": "Аэрофлот",
            "departure": "SVO",
            "arrival": "LED",
            "departure_time": (now + timedelta(hours=3)).isoformat() + "Z",
            "arrival_time": (now + timedelta(hours=5)).isoformat() + "Z",
            "price": 8500,
            "seats_available": 50,
            "status": "scheduled",
        },
        {
            "flight_number": "S7123",
            "airline": "S7 Airlines",
            "departure": "DME",
            "arrival": "KZN",
            "departure_time": (now + timedelta(hours=6)).isoformat() + "Z",
            "arrival_time": (now + timedelta(hours=8)).isoformat() + "Z",
            "price": 7200,
            "seats_available": 42,
            "status": "scheduled",
        },
        {
            "flight_number": "DP456",
            "airline": "Pobeda",
            "departure": "VKO",
            "arrival": "AER",
            "departure_time": (now + timedelta(hours=2)).isoformat() + "Z",
            "arrival_time": (now + timedelta(hours=4)).isoformat() + "Z",
            "price": 5400,
            "seats_available": 60,
            "status": "scheduled",
        },
    ]

    db.flights.insert_many(flights)
    print(f"[OK] Добавлено рейсов: {len(flights)}")


def seed_bookings():
    """
    Тестовые бронирования — опционально.
    """
    flights = list(db.flights.find({}))
    if not flights:
        print("[WARN] Нет рейсов — пропускаю бронирования")
        return

    sample_flight = flights[0]

    booking = {
        "booking_ref": "FBT-TEST01",
        "flight_id": str(sample_flight["_id"]),
        "passenger": "Иван Иванов",
        "email": "ivan@example.com",
        "phone": "+79998887766",
        "booking_time": datetime.utcnow().isoformat(),
        "total_price": sample_flight["price"],
        "has_luggage": False,
        "status": "confirmed",
    }

    db.bookings.insert_one(booking)
    print("[OK] Добавлено тестовое бронирование")


def init_database():
    print("=== Инициализация базы данных ===")
    reset_collections()
    seed_airlines()
    seed_flights()
    seed_bookings()
    print("=== Готово! ===")


if __name__ == "__main__":
    init_database()

def init_database():
    print("Initializing database...")

    # Очистка коллекций
    db.airlines.drop()
    db.flights.drop()
    db.bookings.drop()
    db.users.drop()  # ← добавили

    # --- USERS ---
    from api_tester.backend.app.core.security import hash_password

    users = [
        {
            "email": "admin@example.com",
            "password": hash_password("admin123"),
            "role": "admin"
        },
        {
            "email": "test@example.com",
            "password": hash_password("test123"),
            "role": "user"
        }
    ]

    db.users.insert_many(users)
    print("Users inserted.")

    # --- AIRLINES ---
    db.airlines.insert_many([
        {"name": "Аэрофлот", "code": "SU"},
        {"name": "S7 Airlines", "code": "S7"},
        {"name": "UTair", "code": "UT"},
        {"name": "Pobeda", "code": "DP"},
    ])

    # --- FLIGHTS ---
    # (оставляешь свои данные)

    # --- BOOKINGS ---
    # (оставляешь пустым)
