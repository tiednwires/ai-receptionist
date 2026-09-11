from enum import Enum
from typing import Optional

from pydantic import BaseModel

class ProjectType(str, Enum):
    interior = "interior"
    exterior = "exterior"
    both = "both"


class ReceptionistIntakeRequest(BaseModel):
    customer_name: str
    phone_number: str
    property_address: str
    project_type: ProjectType
    project_scope: str
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None
    additional_notes: Optional[str] = None

class ReceptionistIntakeResponse(BaseModel):
    status: str
    message: str
    customer_name: str
    project_type: ProjectType