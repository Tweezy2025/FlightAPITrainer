from pydantic import BaseModel, EmailStr
from typing import List, Optional


# -----------------------------
# Модель пассажира (для bulk)
# -----------------------------
class Passenger(BaseModel):
    name: str
    email: EmailStr
    phone: str
    has_luggage: bool
    seat_preference: Optional[str] = None


# -----------------------------
# Одиночное бронирование
# -----------------------------
class BookingCreateSingle(BaseModel):
    flight_number: str
    passenger: str
    email: EmailStr
    phone: str
    has_luggage: bool


# -----------------------------
# Массовое бронирование
# -----------------------------
class BookingCreateBulk(BaseModel):
    flight_number: str
    promo_code: Optional[str] = None
    notes: Optional[str] = None
    passengers: List[Passenger]


# -----------------------------
# Обновление бронирования
# -----------------------------
class BookingUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    has_luggage: Optional[bool] = None
