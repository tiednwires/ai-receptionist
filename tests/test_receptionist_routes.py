import pytest
from fastapi.testclient import TestClient

import app.routes.receptionist as receptionist_routes
from app.main import app
from app.services.intake_service import IntakeService


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    # Replace the routes module's shared service with a fresh service for each test.
    # This prevents stored customers from leaking between separate tests.
    monkeypatch.setattr(
        receptionist_routes,
        "intake_service",
        IntakeService(),
    )

    # TestClient sends requests directly to the FastAPI app without Uvicorn.
    return TestClient(app)

def test_get_intakes_start_empty(client: TestClient) -> None:
    # Act: request all intakes from a fresh application service.
    response = client.get("/receptionist/intakes")

    # Assert: the route succeeds and returns an empty JSON list.
    assert response.status_code == 200
    assert response.json() == []


def test_create_intake_is_returned_by_get(client: TestClient) -> None:
    # Arrange: build the JSON body a real caller would submit.
    intake_data = {
        "customer_name": "Maria Hernandez",
        "phone_number": "312-555-0148",
        "property_address": "1834 W Addison St, Chicago, IL",
        "project_type": "interior",
        "project_scope": "Paint the living room and kitchen",
        "preferred_date": "2026-09-24",
        "preferred_time": "morning",
        "additional_notes": "Please call before arriving",
    }

    # Act: submit the intake through the POST route.
    post_response = client.post(
        "/receptionist/intake",
        json=intake_data,
    )

    # Assert: the route accepted the intake and returned its confirmation.
    assert post_response.status_code == 200
    assert post_response.json() == {
        "status": "received",
        "message": "Customer intake received successfully.",
        "customer_name": "Maria Hernandez",
        "project_type": "interior",
    }

    # Act: retrieve all intakes during the same application process.
    get_response = client.get("/receptionist/intakes")

    # Assert: GET returns the complete intake submitted through POST.
    assert get_response.status_code == 200
    assert get_response.json() == [intake_data]


def test_create_intake_rejects_invalid_project_type(
    client: TestClient,
) -> None:
    # Arrange: provide a project type outside interior, exterior, or both.
    invalid_intake = {
        "customer_name": "Taylor Morgan",
        "phone_number": "312-555-0110",
        "property_address": "900 W Chicago Ave, Chicago, IL",
        "project_type": "roofing",
        "project_scope": "Replace the roof",
    }

    # Act: submit the invalid request.
    response = client.post(
        "/receptionist/intake",
        json=invalid_intake,
    )

    # Assert: FastAPI rejects it as an unprocessable request.
    assert response.status_code == 422


def test_create_intake_rejects_missing_phone_number(
    client: TestClient,
) -> None:
    # Arrange: missing phone_number, which the intake model requires.
    incomplete_intake = {
        "customer_name": "Alex Johnson",
        "property_address": "1200 N Clark St, Chicago, IL",
        "project_type": "both",
        "project_scope": "Paint the interior and exterior",
    }

    # Act: submit the incomplete request.
    response = client.post(
        "/receptionist/intake",
        json=incomplete_intake,
    )

    # Assert: validation fails and identifies phone_number as missing.
    assert response.status_code == 422

    error_fields = {
        error["loc"][-1]
        for error in response.json()["detail"]
    }
    assert "phone_number" in error_fields


def test_get_business_information_returns_approved_answer(
    client: TestClient,
) -> None:
    # Act: request a recognized topic through the API.
    response = client.get(
        "/receptionist/business-information/business-hours"
    )

    # Assert: the route returns the approved answer.
    assert response.status_code == 200
    assert response.json() == {
        "topic": "business-hours",
        "answer": "Monday through Friday, 8:00 AM to 5:00 PM.",
    }


def test_get_business_information_returns_404_for_unknown_topic(
    client: TestClient,
) -> None:
    # Act: request a topic that has no approved answer.
    response = client.get(
        "/receptionist/business-information/pricing"
    )

    # Assert: the route reports that the information was not found.
    assert response.status_code == 404
    assert response.json() == {
        "detail": (
            "Approved business information was not found for this topic."
        )
    }