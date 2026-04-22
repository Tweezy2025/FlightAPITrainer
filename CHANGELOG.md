# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to **Semantic Versioning**.

---

## [0.2.0] - 2026-04-22

### Added
- **Payments module**
  - Implemented `Payment` model (ID, booking reference, amount, method, status, timestamps)
  - Added `PaymentService` with:
    - create payment
    - get payment
    - cancel payment
  - Added API endpoints:
    - `POST /api/payments/` — create a payment
    - `GET /api/payments/{payment_id}` — retrieve a payment
    - `DELETE /api/payments/{payment_id}` — cancel a payment
  - Full MongoDB integration
  - Added unit tests for service logic
  - Added integration tests for API
  - Added e2e tests
  - Allure report: **100% passed**

### Changed
- Refactored `main.py`:
  - removed duplicate FastAPI initialization
  - unified router registration
  - added payments router under `/api/payments`
- Updated integration tests to use correct API paths
- Improved router structure consistency across modules

### Fixed
- Fixed missing payments routes inside Docker test container
- Fixed PYTHONPATH issues preventing `api_tester` package imports
- Fixed incorrect relative imports in `main.py`

---

## [Unreleased]
- Notifications module (in progress)
- RabbitMQ integration (planned)
