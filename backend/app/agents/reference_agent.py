from app.schemas import SecurityReference, Threat
from app.services.reference_service import ReferenceService


class ReferenceAgent:
    def __init__(self, reference_service: ReferenceService | None = None) -> None:
        self.reference_service = reference_service or ReferenceService()

    def run(self, threats: list[Threat], report_language: str = "en") -> list[SecurityReference]:
        return self.reference_service.map_threats(threats, report_language=report_language)
