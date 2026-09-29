"""Apply deterministic rules to proposed estimate appointments."""

from datetime import date, time, timedelta

from app.models.scheduling import (
    EstimateSchedulingRequest,
    EstimateSchedulingResponse,
)


# Estimates may be requested during normal weekday business hours.
BUSINESS_OPEN_TIME = time(hour=8)
LATEST_ESTIMATE_START_TIME = time(hour=16)

# The business allows appointments to be proposed at most 30 days ahead.
MAX_DAYS_AHEAD = 30


class SchedulingService:
    """Determine whether proposed estimate appointments follow business rules."""

    def evaluate_request(
        self,
        request: EstimateSchedulingRequest,
        today: date | None = None,
    ) -> EstimateSchedulingResponse:
        """Evaluate one request and explain whether it is allowed."""

        # Tests can supply a fixed date. Normal application calls use today.
        reference_date = today or date.today()
        requested_date = request.requested_date
        requested_time = request.requested_time

        if requested_date <= reference_date:
            return EstimateSchedulingResponse(
                allowed=False,
                reason="Estimates must be scheduled after today.",
                requested_date=requested_date,
                requested_time=requested_time,
            )

        if requested_date > reference_date + timedelta(days=MAX_DAYS_AHEAD):
            return EstimateSchedulingResponse(
                allowed=False,
                reason="Estimates may be scheduled up to 30 days in advance.",
                requested_date=requested_date,
                requested_time=requested_time,
            )

        # weekday() uses 0 through 4 for Monday through Friday.
        if requested_date.weekday() >= 5:
            return EstimateSchedulingResponse(
                allowed=False,
                reason="Estimates are available Monday through Friday.",
                requested_date=requested_date,
                requested_time=requested_time,
            )

        if not BUSINESS_OPEN_TIME <= requested_time <= LATEST_ESTIMATE_START_TIME:
            return EstimateSchedulingResponse(
                allowed=False,
                reason="Estimates must start between 8:00 AM and 4:00 PM.",
                requested_date=requested_date,
                requested_time=requested_time,
            )

        return EstimateSchedulingResponse(
            allowed=True,
            reason="The proposed estimate time is available.",
            requested_date=requested_date,
            requested_time=requested_time,
        )


# Create one shared service instance for future API routes to reuse.
scheduling_service = SchedulingService()
