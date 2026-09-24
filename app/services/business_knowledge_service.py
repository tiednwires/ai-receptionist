"""Provide approved business information from a local JSON file."""

import json
from pathlib import Path


# Build an absolute path to config/business.json from this file's location.
# parents[2] moves from app/services to the repository root.
DEFAULT_BUSINESS_DATA_PATH = (
    Path(__file__).resolve().parents[2] / "config" / "business.json"
)


class BusinessKnowledgeService:
    """Load and provide the business's approved FAQ answers."""

    def __init__(
        self,
        data_path: Path = DEFAULT_BUSINESS_DATA_PATH,
    ) -> None:
        # Read the JSON file once when this service instance is created.
        with data_path.open(encoding="utf-8") as data_file:
            self._information: dict[str, str] = json.load(data_file)

    def get_business_information(self, topic: str) -> str | None:
        """Return the approved answer for a topic, or None when it is unknown."""

        # Normalize common input differences:
        # "Business Hours", "business-hours", and "business_hours"
        # all become "business_hours".
        normalized_topic = (
            topic.strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        return self._information.get(normalized_topic)


# Create one shared service instance for the application to share.
business_knowledge_service = BusinessKnowledgeService()
