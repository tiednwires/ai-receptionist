from fastapi import APIRouter

from app.models.receptionist import (
    ReceptionistIntakeRequest,
    ReceptionistIntakeResponse,
)

router = APIRouter(prefix="/receptionist", tags=["receptionist"])


@router.post("/intake", response_model=ReceptionistIntakeResponse)
def create_intake(request: ReceptionistIntakeRequest) -> ReceptionistIntakeResponse:
    return ReceptionistIntakeResponse(
        status="received",
        message="Customer intake received successfully.",
        customer_name=request.customer_name,
        project_type=request.project_type,
    )
