# Development Log

## 2026-09-18 - In-memory intake service

### Work completed

- Added `IntakeService` to separate intake storage from the API route.
- Added temporary in-memory storage for validated receptionist intakes.
- Added `create_intake()` to store and return an intake.
- Added `get_all_intakes()` to return a copy of the stored intake list.
- Created one shared `intake_service` instance.
- Updated `POST /receptionist/intake` to store validated requests through the service.
- Added `GET /receptionist/intakes` to retrieve stored intakes.

### Verification

- Tested `IntakeService` directly from Python.
- Confirmed the FastAPI application imports successfully.
- Confirmed Swagger displays both receptionist endpoints.
- Submitted a realistic painting customer intake through Swagger.
- Received HTTP `200 OK` from the POST endpoint.
- Retrieved the complete intake through the GET endpoint.
- Confirmed data persists across requests while the Uvicorn process is running.

### Current limitation

Storage is intentionally temporary and in memory. Restarting or reloading the application clears all submitted intakes. A database has not been introduced.

### Next step

Add automated tests for the intake service and receptionist API routes before beginning any database, LLM, telephony, or Google Calendar integration.


## 2026-09-22 - Automated service and API tests

### Work completed

- Added `requirements-dev.txt`.
- Added pytest as the automated test runner.
- Added HTTPX for FastAPI `TestClient` support.
- Added three automated tests for `IntakeService`.
- Added four automated tests for the receptionist API routes.
- Used a pytest fixture and monkeypatching to provide a fresh `IntakeService` for every API test.

### Verification

- Confirmed a new `IntakeService` starts empty.
- Confirmed `create_intake()` stores and returns an intake.
- Confirmed `get_all_intakes()` returns a copy and protects internal state.
- Confirmed `GET /receptionist/intakes` returns an empty list with a fresh service.
- Confirmed an intake submitted through POST is retained and returned through GET during the same application process.
- Confirmed an invalid project type returns HTTP `422`.
- Confirmed a missing required phone number returns HTTP `422` and identifies the missing field.
- Ran the complete suite with `python -m pytest -v`.
- Result: `7 passed`.

### Known warning

The test suite currently reports one deprecation warning from Starlette’s internal `TestClient` integration with AnyIO. The warning originates in an installed dependency and does not cause a test failure.

### Current limitation

Intake storage remains intentionally temporary and in memory. Restarting the application clears all submitted intakes.

### Next step

Add a deterministic business-knowledge service for approved painting-company FAQs, with automated tests, before introducing any LLM or external integration.