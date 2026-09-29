from datetime import date, time

import pytest

from app.models.scheduling import EstimateSchedulingRequest
from app.services.scheduling_service import SchedulingService


def test_allows_valid_weekday_estimate() -> None:
    # Arrange: use a fixed Tuesday as "today" and request Wednesday morning.
    today = date(2026, 9, 29)
    request = EstimateSchedulingRequest(
        requested_date=date(2026, 9, 30),
        requested_time=time(hour=9),
    )
    service = SchedulingService()

    # Act: evaluate the proposed appointment.
    result = service.evaluate_request(request, today=today)

    # Assert: the weekday appointment follows every scheduling rule.
    assert result.allowed is True
    assert result.reason == "The proposed estimate time is available."
    assert result.requested_date == request.requested_date
    assert result.requested_time == request.requested_time


@pytest.mark.parametrize(
    "requested_date",
    [
        date(2026, 9, 29),  # Same day.
        date(2026, 9, 28),  # Past day.
    ],
)
def test_rejects_same_day_and_past_estimates(
    requested_date: date,
) -> None:
    # Arrange: evaluate both dates relative to the same fixed "today."
    today = date(2026, 9, 29)
    request = EstimateSchedulingRequest(
        requested_date=requested_date,
        requested_time=time(hour=9),
    )
    service = SchedulingService()

    # Act.
    result = service.evaluate_request(request, today=today)

    # Assert.
    assert result.allowed is False
    assert result.reason == "Estimates must be scheduled after today."
    assert result.requested_date == requested_date


def test_rejects_weekend_estimate() -> None:
    # Arrange: October 3, 2026 is a Saturday.
    today = date(2026, 9, 29)
    request = EstimateSchedulingRequest(
        requested_date=date(2026, 10, 3),
        requested_time=time(hour=9),
    )
    service = SchedulingService()

    # Act.
    result = service.evaluate_request(request, today=today)

    # Assert.
    assert result.allowed is False
    assert result.reason == "Estimates are available Monday through Friday."


def test_rejects_estimate_more_than_30_days_ahead() -> None:
    # Arrange: October 30 is 31 days after the fixed reference date.
    today = date(2026, 9, 29)
    request = EstimateSchedulingRequest(
        requested_date=date(2026, 10, 30),
        requested_time=time(hour=9),
    )
    service = SchedulingService()

    # Act.
    result = service.evaluate_request(request, today=today)

    # Assert.
    assert result.allowed is False
    assert result.reason == (
        "Estimates may be scheduled up to 30 days in advance."
    )


@pytest.mark.parametrize(
    "requested_time",
    [
        time(hour=7, minute=59),
        time(hour=16, minute=1),
    ],
)
def test_rejects_estimates_outside_business_hours(
    requested_time: time,
) -> None:
    # Arrange: use a valid weekday but an invalid start time.
    today = date(2026, 9, 29)
    request = EstimateSchedulingRequest(
        requested_date=date(2026, 9, 30),
        requested_time=requested_time,
    )
    service = SchedulingService()

    # Act.
    result = service.evaluate_request(request, today=today)

    # Assert.
    assert result.allowed is False
    assert result.reason == (
        "Estimates must start between 8:00 AM and 4:00 PM."
    )


@pytest.mark.parametrize(
    "requested_time",
    [
        time(hour=8),
        time(hour=16),
    ],
)
def test_allows_business_hour_boundaries(
    requested_time: time,
) -> None:
    # Arrange: the opening time and latest start time are both inclusive.
    today = date(2026, 9, 29)
    request = EstimateSchedulingRequest(
        requested_date=date(2026, 9, 30),
        requested_time=requested_time,
    )
    service = SchedulingService()

    # Act.
    result = service.evaluate_request(request, today=today)

    # Assert.
    assert result.allowed is True
    assert result.reason == "The proposed estimate time is available."
