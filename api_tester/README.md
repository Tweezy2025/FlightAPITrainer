# ✈️ Flight Booking Trainer

[🇬🇧 English](#english-version) | [🇷🇺 Русский](#russian-version)

---

# 🇬🇧 English Version

## ✈️ Flight Booking Trainer (FastAPI + MongoDB)

A training project designed to practice API development using **FastAPI**, **MongoDB**, and a clean modular service architecture.

The project includes:

- a fully functional REST API for flights, bookings, and airlines  
- a dedicated service layer (business logic)  
- database initialization script  
- automated tests using pytest + TestClient  
- a simple HTML/JS frontend for manual testing  

---

## 🚀 Features

### ✈️ Flights
- Retrieve a list of flights  
- Filter by:
  - departure airport
  - arrival airport
  - date (YYYY-MM-DD)

### 🧾 Bookings
- Create a single booking  
- Create multiple bookings (bulk)  
- Apply promo codes  
- Automatic seat assignment  
- Retrieve booking details  
- Update booking  
- Cancel booking (with refund info)

### 🛫 Airlines
- Retrieve a list of airlines  

---

## 📦 Technologies Used

- **FastAPI**
- **MongoDB (pymongo)**
- **Uvicorn**
- **Pydantic**
- **pytest + FastAPI TestClient**
- **HTML/JavaScript frontend demo**

---

## 📁 Project Structure
```text
api_tester/
  backend/
    main.py
    app/
      api/
        flights.py
        bookings.py
        airlines.py
        light.py
      services/
        booking_service.py
        flight_service.py
        discount_service.py
        seat_service.py
      db/
        mongo.py
        init_db.py
      core/
        logging.py
      config.py
  frontend/
    index.html
    app.js
    style.css
  tests/
    conftest.py
    test_flights.py
    test_bookings.py
    test_airlines.py
```

---

## ⚙️ Installation & Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```
### 2. Start MongoDB
Using Docker:
```bash
docker run -d -p 27017:27017 mongo
```
### 3. Initialize the database
```bash
python -m api_tester.backend.app.db.init_db
```
### 4. Start the FastAPI server
```bash
uvicorn api_tester.backend.main:app --reload
```
### 5. Open API documentation
Swagger UI
http://localhost:8000/docs
ReDoc:
http://localhost:8000/redoc
### 🧪 Running Tests
Run all tests:
```bash
pytest -q
```
```text
Test coverage includes:
-flight filtering
-single booking
-bulk booking
-insufficient seats error
-booking retrieval
-booking update
-booking cancellation
-airlines endpoint
```
### 🔌 API Examples
Get flights
```bash
GET /api/flights/
```
With filters:
```bash
GET /api/flights/?departure=SVO&arrival=LED&date=2026-04-19
```
Create a single booking
```bash
POST /api/bookings/
{
  "flight_number": "SU100",
  "passenger": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "has_luggage": true
}
```
Bulk booking
```bash
POST /api/bookings/
{
  "flight_number": "SU100",
  "promo_code": "SUMMER2024",
  "passengers": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "has_luggage": true,
      "seat_preference": "window"
    },
    {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+1987654321",
      "has_luggage": false,
      "seat_preference": "aisle"
    }
  ]
}
```
Retrieve a booking
```bash
GET /api/bookings/FBT-ABC123
```
Update a booking
```bash
PATCH /api/bookings/FBT-ABC123
{
  "email": "new@example.com",
  "has_luggage": true
}
```
Cancel a booking
```bash
DELETE /api/bookings/FBT-ABC123
```
### 🧱 Architecture Overview
The project follows a clean layered architecture:
-API layer — routing, validation, HTTP responses

-Service layer — business logic

-Database layer — MongoDB access

-Tests — isolated, using TestClient and init_db

This ensures:

-maintainability

-testability

-scalability

-clean separation of concerns

### 📄 License
MIT (or any other license you prefer).
### 👨‍💻 Author
Created by Tweezy and Copilot AI  as a practical API training project .
Architecture, services, tests, and documentation are fully custom and production‑grade.



## 🇷🇺 Русская версия

# ✈️ Flight Booking Trainer (FastAPI + MongoDB)

Учебный проект для тренировки API‑запросов, построенный на **FastAPI**, **MongoDB** и модульной архитектуре сервисов.

Проект включает:

- полноценный REST API для рейсов, бронирований и авиакомпаний  
- сервисный слой (business logic)  
- init_db для наполнения базы  
- тесты на FastAPI TestClient  
- фронтенд‑демо (HTML + JS) для ручного тестирования  

---

## 🚀 Возможности API

### ✈️ Flights
- Получение списка рейсов  
- Фильтрация по:
  - departure (город вылета)
  - arrival (город прилёта)
  - date (дата вылета)

### 🧾 Bookings
- Создание одиночного бронирования  
- Массовое бронирование (bulk)  
- Промокоды  
- Назначение мест  
- Получение бронирования  
- Обновление бронирования  
- Отмена бронирования  

### 🛫 Airlines
- Получение списка авиакомпаний  

---

## 📦 Технологии

- **FastAPI**
- **MongoDB (pymongo)**
- **Uvicorn**
- **Pydantic**
- **pytest + TestClient**
- **HTML/JS frontend demo**

---

## 📁 Структура проекта
```text
api_tester/
  backend/
    main.py
    app/
      api/
        flights.py
        bookings.py
        airlines.py
        light.py
      services/
        booking_service.py
        flight_service.py
        discount_service.py
        seat_service.py
      db/
        mongo.py
        init_db.py
      core/
        logging.py
      config.py
  frontend/
    index.html
    app.js
    style.css
  tests/
    conftest.py
    test_flights.py
    test_bookings.py
    test_airlines.py
```

---

## ⚙️ Установка и запуск

### 1. Установить зависимости

```bash
pip install -r requirements.txt
### 1. Install dependencies

```bash
pip install -r requirements.txt
```
### 2. Запустить MongoDB
Using Docker:
```bash
docker run -d -p 27017:27017 mongo
```
### 3. Инициализировать базу
```bash
python -m api_tester.backend.app.db.init_db
```
### 4. Запустить сервер
```bash
uvicorn api_tester.backend.main:app --reload
```
### 5. Открыть документацию
Swagger UI
http://localhost:8000/docs
ReDoc:
http://localhost:8000/redoc
### 🧪 Тестирование
Run all tests:
```bash
pytest -q
```

Покрытие тестов:

-фильтрация рейсов

-одиночное бронирование

-массовое бронирование

-ошибка недостатка мест

-получение бронирования

-обновление

-отмена

-авиакомпании

### 🔌 Примеры API‑запросов
Получить рейсы
```bash
GET /api/flights/
```
Фильтрация:
```bash
GET /api/flights/?departure=SVO&arrival=LED&date=2026-04-19
```
Создать одиночное бронирование
```bash
POST /api/bookings/
{
  "flight_number": "SU100",
  "passenger": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "has_luggage": true
}
```
Массовое бронирование
```bash
POST /api/bookings/
{
  "flight_number": "SU100",
  "promo_code": "SUMMER2024",
  "passengers": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "has_luggage": true,
      "seat_preference": "window"
    },
    {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+1987654321",
      "has_luggage": false,
      "seat_preference": "aisle"
    }
  ]
}
```
Получить бронирование
```bash
GET /api/bookings/FBT-ABC123
```
Обновить бронирование
```bash
PATCH /api/bookings/FBT-ABC123
{
  "email": "new@example.com",
  "has_luggage": true
}
```
Отменить бронирование
```bash
DELETE /api/bookings/FBT-ABC123
```
### 🧱 Архитектура
Проект построен по принципу:

API‑слой — маршруты, валидация, HTTP‑коды

Service‑слой — бизнес‑логика

DB‑слой — только подключение к MongoDB

Тесты — изолированные, с init_db перед запуском

### 📄 Лицензия
MIT (или любая другая).
### 👨‍💻 Автор
Проект создан Tweezy и Copilot AI как учебный тренажёр API.
Архитектура, сервисы, тесты и документация — полностью кастомные и профессиональные.