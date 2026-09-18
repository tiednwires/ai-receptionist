# AI Receptionist Project Status

Last updated: 2026-09-18

## Project Goal
Build an AI phone receptionist for a residential painting business. The system should answer customer calls, handle basic questions, collect job details, and help schedule appointments.

## Current Business Scope
- Business type: Residential painting contractor
- Primary users: Homeowners calling for painting services
- Calendar system: Google Calendar
- Source control: GitHub
- Backend framework: FastAPI

## Current Repository Structure
```text
ai-receptionist/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── routes/
│   └── services/
├── config/
├── docs/
├── src/
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Environment
- Development machine: macOS
- Python virtual environment: `.venv`
- Virtual environment activation command:
  ```bash
  source .venv/bin/activate
  ```
- Dependencies are installed from `requirements.txt`.

## Backend Status
The FastAPI application is running successfully.

Development server command:

```bash
python -m uvicorn app.main:app --reload --reload-exclude ".venv/*"
```

The `.venv` exclusion prevents Uvicorn's file watcher from repeatedly restarting when package files change.

### Verified Endpoints

```text
GET /health
POST /receptionist/intake
GET /receptionist/intakes
```

The health endpoint returns HTTP `200 OK`.

The POST endpoint accepts a validated residential painting intake, stores it through `IntakeService`, and returns HTTP `200 OK`.

The GET endpoint returns every intake stored during the current application process. Testing confirmed that a customer submitted through POST could be retrieved through GET with all fields intact.

This verifies that the receptionist router, Pydantic models, and shared in-memory service are working together correctly.

## Packages Currently Used
The project currently includes:
- FastAPI
- Uvicorn
- pydantic-settings

## Decisions Made So Far
1. The initial use case will focus on a home-painting contractor rather than a generic business.
2. Google Calendar will be used for appointment scheduling.
3. FastAPI will provide the backend/API layer.
4. Development work and documentation will be stored in GitHub.
5. Project decisions, implementation progress, and the exact next step should be recorded in the repository so development does not depend on chat history.
6. API routes should remain thin; intake storage and other business logic belong in service classes.
7. Intake storage is intentionally temporary and in memory at this stage. Restarting the application clears the stored data.
8. A database, LLM, telephony provider, and Google Calendar integration should not be introduced until the current API foundation is tested.

## Planned MVP Capabilities
The first usable version should eventually be able to:
- Receive an incoming phone call through a telephony provider.
- Greet the caller and identify why they are calling.
- Answer basic painting-service questions.
- Collect customer information such as name, phone number, address, and job details.
- Determine whether the caller wants an estimate or appointment.
- Check Google Calendar availability.
- Create an appointment after the caller confirms a time.
- Handle situations it cannot resolve by collecting a message or escalating to a human.

## Current Development Stage
**Stage: Receptionist API foundation**

Completed:
- Repository created.
- Initial Python project structure created.
- Virtual environment created.
- FastAPI and Uvicorn installed.
- Basic FastAPI application created.
- `/health` endpoint created and tested successfully.
- Uvicorn reload configuration corrected to ignore `.venv`.
- Added `ProjectType`, `ReceptionistIntakeRequest`, and `ReceptionistIntakeResponse` Pydantic models.
- Added `POST /receptionist/intake` route.
- Registered the receptionist router with the main FastAPI application.
- Verified the receptionist intake endpoint through Swagger UI with a realistic residential painting customer request and HTTP `200 OK` response.
- Added `IntakeService` with temporary in-memory storage.
- Added `create_intake()` and `get_all_intakes()` service methods.
- Created one shared `intake_service` instance.
- Updated `POST /receptionist/intake` to store validated requests through the service layer.
- Added `GET /receptionist/intakes`.
- Tested the service directly from Python.
- Verified POST and GET through Swagger with a realistic painting customer intake.
- Confirmed the submitted intake remains available across requests while the application process is running.

## Exact Next Step

Add automated tests for `IntakeService` and the receptionist API routes.

The tests should verify intake creation, retrieval, POST/GET retention within one application process, and request validation. Keep storage in memory and do not begin database, LLM, telephony, or Google Calendar integration yet.

## Later Integration Order
A reasonable implementation sequence is:

1. Backend request/response models
2. Receptionist conversation/service logic
3. Google Calendar integration
4. Telephony provider integration
5. Speech-to-text / text-to-speech pipeline
6. LLM conversation orchestration
7. Error handling and human escalation
8. Testing
9. Deployment

## Documentation Rule
Whenever a meaningful architectural decision, feature, dependency, workflow, or implementation change is made, update the project documentation in this repository.

## Resume Instructions

When beginning a new development session:

1. Read this file first.
2. Review the latest entries in development-log.md.
3. Run `git status`.
4. Review recent commits with `git log --oneline -10`.
5. Inspect files related to the Current Development Stage.
6. Continue from Exact Next Step.
7. Do not recreate completed work unless repository state shows it is missing.