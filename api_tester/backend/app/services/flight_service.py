# app/services/flight_service.py
from api_tester.backend.app.db.mongo import db


def get_flight_by_number(flight_number: str) -> dict | None:
    return db.flights.find_one({"flight_number": flight_number})


def decrement_seats(flight_id, count: int = 1):
    db.flights.update_one({"_id": flight_id}, {"$inc": {"seats_available": -count}})


def increment_seats(flight_id, count: int = 1):
    db.flights.update_one({"_id": flight_id}, {"$inc": {"seats_available": count}})
