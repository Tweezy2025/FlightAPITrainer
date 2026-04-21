# ✈️ Flight Booking API

A modular training project demonstrating a production‑style backend architecture using FastAPI, MongoDB, Docker, and automated testing with Allure.  
The project includes a minimal frontend for interacting with the API.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Allure Reports](#allure-reports)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [License](#license)

---

## 📝 Overview

This project implements a Flight Booking API using FastAPI and MongoDB.  
It includes:

- User registration & authentication (JWT)
- Flight listing and filtering
- Single and bulk booking creation
- Booking updates and cancellation
- Automated unit & integration tests
- Allure reporting via Docker

The project is intended as a hands‑on backend training environment with real‑world architecture and tooling.

---

## ⭐ Features

### Authentication
- User registration  
- Login with JWT token  
- Password hashing (bcrypt)

### Flights
- Retrieve all flights  
- Filter by departure, arrival, date

### Bookings
- Create single booking  
- Create bulk booking with seat validation  
- Update booking (price recalculation included)  
- Cancel booking with seat restoration

### Testing & Reporting
- Full pytest suite (unit + integration)  
- Allure reporting with Docker UI  
- Automatic report regeneration

---

## 🧰 Tech Stack

### Backend
- FastAPI  
- Pydantic v2  
- MongoDB + PyMongo  
- Passlib (bcrypt)  
- python‑jose (JWT)

### Testing
- pytest  
- pytest‑anyio  
- pytest‑html  
- allure‑pytest

### Infrastructure
- Docker & Docker Compose  
- Allure Docker Service  
- Allure Docker Service UI

---

## 🏗 Architecture

The system is structured into three main layers:

### Backend (FastAPI)
- Handles authentication, flights, and bookings logic  
- Provides REST API endpoints  
- Uses Pydantic v2 for validation  
- Communicates with MongoDB through a dedicated database layer  

### Database (MongoDB)
- Stores users, flights, and bookings  
- Ensures atomic updates for seat management  

### Testing & Reporting
- pytest for unit and integration tests  
- Allure Docker Service for report generation  
- Allure Docker Service UI for viewing reports  

---

## 📁 Project Structure

```text
api_tester/
│
├── backend/
│   ├── app/
│   │   ├── api/                   # API routers
│   │   ├── core/                  # Auth, logging, security
│   │   ├── db/                    # MongoDB connection
│   │   ├── models/                # Pydantic schemas
│   │   ├── services/              # Business logic
│   │   ├── utils/                 # Config & helpers
│   │   └── main.py                # FastAPI entrypoint
│   └── Dockerfile
│
├── frontend/
│   ├── index.html                 # UI layout
│   ├── app.js                     # API calls
│   ├── style.css                  # Styling
│   └── README.md
│
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── conftest.py                # Fixtures
│   └── Dockerfile
│
├── docker-compose.yml             # Full environment
├── pytest.ini                     # Pytest config
└── README.md
```
## ⚙️ Setup & Installation

### Requirements
- Docker  
- Docker Compose  
- Git

### Clone the repository

```bash
git clone https://github.com/yourname/flight-booking-api.git
cd flight-booking-api
```
### Environment configuration
The project uses default environment variables defined inside docker-compose.yml.
No additional configuration is required for local development.

### Install dependencies (optional, only if running without Docker)
```bash
pip install -r backend/requirements.txt
```
### Start the full environment (recommended)
```bash
docker compose up --build
```
This will start:

- FastAPI backend

- MongoDB

- Allure API

- Allure UI

- Test runner container (on demand)
## 🚀 Running the Application

### Start all services

The recommended way to run the project is via Docker Compose:

```bash
docker compose up --build
```
This command will start:

- FastAPI backend — http://localhost:8000

- MongoDB database — localhost:27017

- Allure API service — http://localhost:5050

- Allure UI dashboard — http://localhost:5252/allure-docker-service-ui/
### Hot reload (development mode)
If you want to run the backend locally without Docker:

```bash
uvicorn backend.app.main:app --reload
```
Make sure MongoDB is running locally or via Docker.
### Verify the API is running
Open:

```
http://localhost:8000/docs
```
This will show the interactive Swagger UI.
## 🧪 Running Tests

### Run the full test suite

To execute all unit and integration tests inside the Docker environment:

```bash
docker compose run --rm tests pytest -vv
```
This will:

- start the test container

- run all tests with verbose output

- generate Allure results into allure-results/

### Run tests locally (optional)
If you prefer running tests without Docker:

```bash
pytest -vv
```
### Make sure dependencies are installed:
```bash
pip install -r backend/requirements.txt
```
### Run a specific test file
```bash
pytest tests/integration/test_bookings.py -vv
```
### Run a specific test case
```bash
pytest tests/unit/test_flights.py::test_filter_by_date -vv
```
### Generate Allure results manually
```bash
pytest --alluredir=allure-results
```
All results will appear in:
```
allure-results/
```
## 📊 Allure Reports

### Start Allure services

To launch the Allure API and UI dashboards:

```bash
docker compose up allure allure-ui
```
This will start:

- Allure API service — http://localhost:5050

- Allure UI dashboard — http://localhost:5252/allure-docker-service-ui/
### View the report
Open the UI in your browser:
```
http://localhost:5252/allure-docker-service-ui/
```

The dashboard automatically loads the latest results from:
```
allure-results/
```
### Regenerate reports manually (optional)
If you want to regenerate results without Docker:
```bash
pytest --alluredir=allure-results
```
Then serve the report locally:
```bash
allure serve allure-results
```
This opens an interactive Allure dashboard in your browser.
## 🔧 Environment Variables

The project uses a minimal set of environment variables.  
All defaults are already defined inside `docker-compose.yml`, so no manual configuration is required for local development.

### Backend environment variables

| Variable | Description | Default |
|---------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://mongo:27017` |
| `MONGODB_DBNAME` | Database name | `api_tester` |
| `JWT_SECRET_KEY` | Secret key for JWT signing | auto-generated in compose |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `30` |

### Frontend environment variables

The frontend supports optional `.env` overrides:

| Variable | Description | Default |
|---------|-------------|---------|
| `API_BASE_URL` | Backend API URL | `http://localhost:8000` |

### Test environment variables

The test container uses its own isolated environment:

| Variable | Description | Default |
|---------|-------------|---------|
| `MONGODB_URI` | MongoDB for tests | `mongodb://mongo:27017` |
| `MONGODB_DBNAME` | Test database | `api_tester` |

### Customizing environment variables

To override any variable, create a `.env` file in the project root:

```bash
MONGODB_URI=mongodb://localhost:27017
JWT_SECRET_KEY=your_secret_key
```
Docker Compose automatically loads .env if present.

## 📡 API Endpoints

Below is a summary of the main REST API endpoints exposed by the backend.

---

### 🔐 Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate user and return JWT token |

---

### ✈️ Flights

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/flights/` | Get all flights |
| GET | `/api/flights/?departure=SVO` | Filter flights by departure airport |
| GET | `/api/flights/?arrival=LED` | Filter flights by arrival airport |
| GET | `/api/flights/?date=2024-12-25` | Filter flights by date |

---

### 🧾 Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/bookings/` | Create a new booking |
| POST | `/api/bookings/bulk` | Create multiple bookings at once |
| GET | `/api/bookings/{reference}` | Get booking by reference |
| PATCH | `/api/bookings/{reference}` | Update booking (recalculate price if needed) |
| DELETE | `/api/bookings/{reference}` | Cancel booking and restore seats |

---

### 🛫 Airlines (optional/public)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/airlines/` | Get list of airlines |

---

### 💡 Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/light/ping` | Simple health check endpoint |


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
## MIT License

Copyright (c) 2026 Tweezy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN  
THE SOFTWARE.
