"""Data models for deterministic estimate scheduling."""

from datetime import date, time

from pydantic import BaseModel


class EstimateSchedulingRequest(BaseModel):
    """Validate a proposed date and time for an on-site estimate."""

    # Using date and time gives us structured values that can be compared
    # reliably instead of manually interpreting arbitrary strings.
    requested_date: date
    requested_time: time


class EstimateSchedulingResponse(BaseModel):
    """Describe whether a proposed time follows the business rules."""

    allowed: bool
    reason: str
    requested_date: date
    requested_time: time
