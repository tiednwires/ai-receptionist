"""Response models for approved business information."""

from pydantic import BaseModel


class BusinessInformationResponse(BaseModel):
    """Define the business-information response returned by the API."""

    # The requested topic and its approved answer are returned together.
    topic: str
    answer: str
