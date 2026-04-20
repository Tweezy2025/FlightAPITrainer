# app/api/flights.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from api_tester.backend.app.db.mongo import db


router = APIRouter()


# -----------------------------
# Pydantic схемы
# -----------------------------

class Flight(BaseModel):
    flight_number: str
    airline: str
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str
    price: float
    seats_available: int
    status: str = "scheduled"


class FlightCreate(BaseModel):
    flight_number: str = Field(..., example="SU-1234")
    airline: str = Field(..., example="Аэрофлот")
    departure: str = Field(..., example="SVO")
    arrival: str = Field(..., example="LED")
    departure_time: str = Field(..., example="2024-12-25T10:30:00Z")
    arrival_time: str = Field(..., example="2024-12-25T13:45:00Z")
    price: float = Field(..., example=8500.00)
    seats_available: int = Field(..., example=56)


# -----------------------------
# Эндпоинты
# -----------------------------

@router.get("/", response_model=List[Flight])
def search_flights(
    departure: Optional[str] = Query(None, description="Код аэропорта отправления"),
    arrival: Optional[str] = Query(None, description="Код аэропорта прибытия"),
    date: Optional[str] = Query(None, description="Дата вылета YYYY-MM-DD")
):
    """
    Поиск рейсов по фильтрам:
    - departure
    - arrival
    - date (фильтрация по дате вылета)
    """

    query = {}

    if departure:
        query["departure"] = departure

    if arrival:
        query["arrival"] = arrival

    if date:
        query["departure_time"] = {
            "$gte": f"{date}T00:00:00Z",
            "$lt": f"{date}T23:59:59Z"
        }

    flights = list(db.flights.find(query, {"_id": 0}))
    return flights


@router.post("/", response_model=dict, status_code=201)
def add_flight(data: FlightCreate):
    """
    Добавление нового рейса.
    """

    # Проверяем, что рейса с таким номером нет
    existing = db.flights.find_one({"flight_number": data.flight_number})
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Рейс {data.flight_number} уже существует"
        )

    flight = data.dict()
    flight["status"] = "scheduled"

    db.flights.insert_one(flight)

    return {
        "message": "Рейс добавлен успешно",
        "flight_number": data.flight_number
    }
