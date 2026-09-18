"""Temporary in-memory storage for validated receptionist intakes."""

# Import the Pydantic model that represents a validated customer intake.
# The service will store the same structured objects created by FastAPI.
from app.models.receptionist import ReceptionistIntakeRequest


class IntakeService:
    """Store and retrieve intakes during the current application process."""

    def __init__(self) -> None:
        # Create an empty list whenever an IntakeService instance is created.
        # Each item must be a validated ReceptionistIntakeRequest object.
        #
        # The leading underscore marks this as internal service state. Other
        # modules should use the methods below instead of changing it directly.
        self._intakes: list[ReceptionistIntakeRequest] = []

    def create_intake(
        self,
        request: ReceptionistIntakeRequest,
    ) -> ReceptionistIntakeRequest:
        """Store one validated intake and return the stored object."""

        # Add the intake to the end of the in-memory list.
        self._intakes.append(request)

        # Return the object so a caller can use its values after storage.
        return request

    def get_all_intakes(self) -> list[ReceptionistIntakeRequest]:
        """Return a copy of every intake stored by this service instance."""

        # Returning a copy prevents outside code from directly appending,
        # removing, or reordering items in the service's internal list.
        return self._intakes.copy()


# Create one shared service object for the application to import later.
# Routes using this same object will share its list until the process restarts.
# Restarting Uvicorn creates a new instance, so this is not permanent storage.
intake_service = IntakeService()
