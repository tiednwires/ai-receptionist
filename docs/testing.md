# Testing Guide

## Setup

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

## Run the Complete Test Suite

```bash
python -m pytest -v
```

Current expected result:

```text
12 passed
```

## Run One Test File

Intake-service tests:

```bash
python -m pytest tests/test_intake_services.py -v
```

Business-knowledge service tests:

```bash
python -m pytest tests/test_business_knowledge_service.py -v
```

Receptionist API tests:

```bash
python -m pytest tests/test_receptionist_routes.py -v
```

## Current Test Coverage

The suite verifies:

- In-memory intake creation and retrieval.
- Protection of the intake service’s internal list.
- API validation of required fields and project types.
- Isolation of stored intakes between API tests.
- Loading approved business answers from local JSON.
- Normalization of business-information topics.
- HTTP `200` responses for recognized business topics.
- HTTP `404` responses for unknown business topics.

## Known Warning

The suite may report a deprecation warning from Starlette’s internal `TestClient` integration with AnyIO. This warning originates in an installed dependency and does not cause a test failure.