from app.services.business_knowledge_service import BusinessKnowledgeService


def test_returns_approved_business_hours() -> None:
    # Arrange create a service using the approved business JSON file.
    service = BusinessKnowledgeService()

    # Act: request a recognized topic.
    answer = service.get_business_information("business hours")

    # Assert: the service returns the approved answer from the JSON file.
    assert answer == "Monday through Friday, 8:00 AM to 5:00 PM."


def test_returns_none_for_unknown_topic() -> None:
    # Arrange: create a service using the approved business info.
    service = BusinessKnowledgeService()

    # Act: request info that is not in the approved JSON file.
    answer = service.get_business_information("pricing")

    # Assert: the service clearly reports that no approved answer exists.
    assert answer is None


def test_normalizes_topic_format() -> None:
    # Arrange: create one service and define the approved answer.
    service = BusinessKnowledgeService()
    expected_answer = "Monday through Friday, 8:00 AM to 5:00 PM."

    # Assert: spacing, capitalization, and separators normalize to one key.
    assert (
        service.get_business_information("  Business Hours  ")
        == expected_answer
    )
    assert (
        service.get_business_information("business-hours")
        == expected_answer
    )
    assert (
        service.get_business_information("business_hours")
        == expected_answer
    )
