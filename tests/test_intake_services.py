from app.models.receptionist import ReceptionistIntakeRequest
from app.services.intake_service import IntakeService

def test_create_intake_stores_and_returns_intake() -> None:
    # Arrange: create a fresh service and realistic customer intake.
    service = IntakeService()

    intake = ReceptionistIntakeRequest(
        customer_name="Maria Hernandez",
        phone_number="312-555-0148",
        property_address="1834 W Addison St, Chicago, IL",
        project_type="interior",
        project_scope="Paint the living room and kitchen",
        preferred_date="2026-09-24",
        preferred_time="morning",
        additional_notes="Please call before arriving",
    )

    # Act: ask the service to store the intake.
    saved_intake = service.create_intake(intake)


    # Assert: the service returned and retained the same intake.
    assert saved_intake == intake
    assert service.get_all_intakes() == [intake]



def test_new_service_starts_with_no_intakes() -> None:
    # Arrange: create a completeley new service instance.
    service = IntakeService()

    # Assert: a new service should contain no customer intakes.
    assert service.get_all_intakes() == []



def test_get_all_intakes_returns_a_copy() -> None:
    # Arrange: create a service containing one intake.
    service = IntakeService()

    intake = ReceptionistIntakeRequest(
        customer_name="Jordan Lee",
        phone_number="312-555-0199",
        property_address="500 N State St, Chicago, IL",
        project_type="exterior",
        project_scope="Paint the exterior siding",
    )

    service.create_intake(intake)

    # Act: retrieve the list and modify the returmed copy.
    returned_intakes = service.get_all_intakes()
    returned_intakes.clear()

    # Assert: modifying the returned list did not erase the sevice's data.
    assert service.get_all_intakes() == [intake]