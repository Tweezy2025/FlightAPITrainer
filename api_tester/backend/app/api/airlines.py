# app/api/airlines.py
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

from api_tester.backend.app.db.mongo import db


router = APIRouter()


# -----------------------------
# Pydantic-схемы
# -----------------------------

class Airline(BaseModel):
    name: str
    code: str


# -----------------------------
# Эндпоинты
# -----------------------------

@router.get("/", response_model=List[Airline])
def get_airlines():
    """
    Получить список всех авиакомпаний.
    """
    airlines = list(db.airlines.find({}, {"_id": 0}))
    if not airlines:
        # Не обязательно, но можно явно подсветить пустую БД
        raise HTTPException(status_code=404, detail="Авиакомпании не найдены")
    return airlines
