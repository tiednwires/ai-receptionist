

# AI Receptionist Project Status

Last updated: 2026-09-11

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

### Verified Endpoint

```text
GET /health
```

Current response:

```json
{"status":"healthy"}
```

The endpoint returned HTTP `200 OK`, confirming the local backend is working.

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
**Stage: Backend foundation**

Completed:
- Repository created.
- Initial Python project structure created.
- Virtual environment created.
- FastAPI and Uvicorn installed.
- Basic FastAPI application created.
- `/health` endpoint created and tested successfully.
- Uvicorn reload configuration corrected to ignore `.venv`.

## Exact Next Step
Design and implement the first receptionist API layer before adding telephony or AI-model integration.

The next development task is to define the basic call/customer data models and create an initial API route that represents an incoming receptionist interaction. This gives us a clean backend contract before connecting a phone provider, an LLM, or Google Calendar.

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