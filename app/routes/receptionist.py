"""HTTP endpoints for the receptionist intake workflow."""

# APIRouter groups related endpoints so they can be registered together.
from fastapi import APIRouter

# Import the shared intake service so every receptionist route can use the
# same temporary in-memory storage while the application is running.
from app.services.intake_service import intake_service

# The request model validates incoming JSON. The response model defines and
# validates the JSON returned to the caller.
from app.models.receptionist import (
    ReceptionistIntakeRequest,
    ReceptionistIntakeResponse,
)

# Every route in this module begins with /receptionist. The tag groups these
# endpoints together in FastAPI's generated Swagger documentation.
router = APIRouter(prefix="/receptionist", tags=["receptionist"])


# response_model tells FastAPI which response shape to validate and document.
@router.post("/intake", response_model=ReceptionistIntakeResponse)
def create_intake(
    request: ReceptionistIntakeRequest,
) -> ReceptionistIntakeResponse:
    """Store a validated painting-project intake and return confirmation."""

    # Pass the validated request to the service so it is retained in memory.
    saved_intake = intake_service.create_intake(request)

    # Build the API response using the intake returned by the service.
    return ReceptionistIntakeResponse(
        status="received",
        message="Customer intake received successfully.",
        customer_name=saved_intake.customer_name,
        project_type=saved_intake.project_type,
    )


@router.get(
    "/intakes",
    response_model=list[ReceptionistIntakeRequest],
)
def get_intakes() -> list[ReceptionistIntakeRequest]:
    """Return every intake stored during the current application process."""

    # Ask the service for a copy of its current in-memory intake list.
    return intake_service.get_all_intakes()
