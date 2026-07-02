from app.schemas import ArchitectureModel, Countermeasure, SecurityReference, Threat, VulnerabilityFinding
from app.services.report_service import ReportService


class ReportAgent:
    def __init__(self, report_service: ReportService | None = None) -> None:
        self.report_service = report_service or ReportService()

    def run(
        self,
        architecture: ArchitectureModel,
        threats: list[Threat],
        vulnerabilities: list[VulnerabilityFinding],
        countermeasures: list[Countermeasure],
        references: list[SecurityReference],
        report_language: str = "en",
    ) -> str:
        return self.report_service.render_markdown(
            architecture=architecture,
            threats=threats,
            vulnerabilities=vulnerabilities,
            countermeasures=countermeasures,
            references=references,
            report_language=report_language,
        )
