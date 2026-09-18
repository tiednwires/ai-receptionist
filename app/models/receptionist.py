"""Data models for the receptionist intake workflow."""

# Enum restricts a value to a predefined set of named choices.
from enum import Enum

# Optional marks fields that may contain either their stated type or None.
from typing import Optional

# BaseModel provides parsing, validation, serialization, and API schema data.
from pydantic import BaseModel


class ProjectType(str, Enum):
    """Painting project categories accepted by the receptionist."""

    # Inheriting from str makes these enum values serialize cleanly as JSON.
    interior = "interior"
    exterior = "exterior"
    both = "both"


class ReceptionistIntakeRequest(BaseModel):
    """Validate the customer and project information sent to the API."""

    # These fields are required because they do not have default values.
    customer_name: str
    phone_number: str
    property_address: str
    project_type: ProjectType
    project_scope: str

    # These fields are optional. If a caller does not provide one, its value
    # defaults to None rather than causing request validation to fail.
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None
    additional_notes: Optional[str] = None


class ReceptionistIntakeResponse(BaseModel):
    """Define the confirmation returned after an intake is accepted."""

    status: str
    message: str
    customer_name: str
    project_type: ProjectType
