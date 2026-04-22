from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорт роутеров (абсолютные импорты внутри пакета)
from api_tester.backend.app.api.flights import router as flights_router
from api_tester.backend.app.api.bookings import router as bookings_router
from api_tester.backend.app.api.airlines import router as airlines_router
from api_tester.backend.app.api.light import router as light_router
from api_tester.backend.app.api.auth import router as auth_router
from api_tester.backend.app.api.payments import router as payments_router

# Конфиг
from api_tester.backend.app.config import DEBUG_MODE


def create_app() -> FastAPI:
    app = FastAPI(
        title="Flight Booking API Trainer",
        description="Учебный API для тренировки запросов (рейсы, бронирования, авиакомпании)",
        version="1.0.0"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Регистрация роутеров
    app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
    app.include_router(flights_router, prefix="/api/flights", tags=["Flights"])
    app.include_router(bookings_router, prefix="/api/bookings", tags=["Bookings"])
    app.include_router(airlines_router, prefix="/api/airlines", tags=["Airlines"])
    app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
    app.include_router(light_router, tags=["Light"])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api_tester.backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG_MODE
    )
