# app/services/seat_service.py
import random


def assign_seat(preference: str | None = None) -> str:
    """
    Назначение места с учётом предпочтений.
    """
    rows = range(1, 20)
    seats = ["A", "B", "C", "D", "E", "F"]

    if preference == "window":
        seats = ["A", "F"]
    elif preference == "aisle":
        seats = ["B", "E"]

    return f"{random.choice(rows)}{random.choice(seats)}"
