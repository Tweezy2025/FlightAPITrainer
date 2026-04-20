# app/api/light.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "status": "OK",
        "message": "Сервер работает!",
        "version": "1.0.0"
    }
