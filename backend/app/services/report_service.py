from pathlib import Path
from uuid import uuid4

from app.config import settings
from app.schemas import ArchitectureModel, Countermeasure, Threat, VulnerabilityFinding


class ReportService:
    def render_markdown(
        self,
        architecture: ArchitectureModel,
        threats: list[Threat],
        vulnerabilities: list[VulnerabilityFinding],
        countermeasures: list[Countermeasure],
        report_language: str = "en",
    ) -> str:
        if report_language == "pt-BR":
            return self._render_pt_br(architecture, threats, vulnerabilities, countermeasures)
        return self._render_en(architecture, threats, vulnerabilities, countermeasures)

    def _render_en(
        self,
        architecture: ArchitectureModel,
        threats: list[Threat],
        vulnerabilities: list[VulnerabilityFinding],
        countermeasures: list[Countermeasure],
    ) -> str:
        lines = [
            "# ThreatGraph AI STRIDE Report",
            "",
            "## Architecture Summary",
            f"- Components: {len(architecture.components)}",
            f"- Flows: {len(architecture.flows)}",
            f"- Trust boundaries: {len(architecture.trust_boundaries)}",
            "",
            "## Component Overview",
        ]
        lines.extend(self._component_lines(architecture, language="en"))
        lines.extend(["", "## Threats"])

        if not threats:
            lines.append("- No threats generated from the current evidence.")

        for threat in threats:
            lines.extend(
                [
                    f"### {threat.id} - {threat.stride_category}",
                    f"- Severity: {threat.severity}",
                    f"- Confidence: {threat.confidence}",
                    f"- Evidence: {threat.evidence}",
                    f"- Description: {threat.description}",
                    "",
                ]
            )

        lines.extend(["## Vulnerabilities"])
        lines.extend(
            f"- {finding.threat_id}: {finding.weakness} ({finding.confidence})"
            for finding in vulnerabilities
        )
        lines.extend(["", "## Countermeasures"])
        lines.extend(
            f"- {item.threat_id}: {item.recommendation} Priority: {item.priority}."
            for item in countermeasures
        )

        return "\n".join(lines).strip() + "\n"

    def _render_pt_br(
        self,
        architecture: ArchitectureModel,
        threats: list[Threat],
        vulnerabilities: list[VulnerabilityFinding],
        countermeasures: list[Countermeasure],
    ) -> str:
        lines = [
            "# Relatório STRIDE do ThreatGraph AI",
            "",
            "## Resumo da Arquitetura",
            f"- Componentes: {len(architecture.components)}",
            f"- Fluxos: {len(architecture.flows)}",
            f"- Limites de confiança: {len(architecture.trust_boundaries)}",
            "",
            "## Visão dos Componentes",
        ]
        lines.extend(self._component_lines(architecture, language="pt-BR"))
        lines.extend(["", "## Ameaças"])

        if not threats:
            lines.append("- Nenhuma ameaça foi gerada a partir das evidências atuais.")

        for threat in threats:
            lines.extend(
                [
                    f"### {threat.id} - {threat.stride_category}",
                    f"- Severidade: {threat.severity}",
                    f"- Confiança: {threat.confidence}",
                    f"- Evidência: {threat.evidence}",
                    f"- Descrição: {threat.description}",
                    "",
                ]
            )

        lines.extend(["## Vulnerabilidades"])
        lines.extend(
            f"- {finding.threat_id}: {finding.weakness} ({finding.confidence})"
            for finding in vulnerabilities
        )
        lines.extend(["", "## Contramedidas"])
        lines.extend(
            f"- {item.threat_id}: {item.recommendation} Prioridade: {item.priority}."
            for item in countermeasures
        )

        return "\n".join(lines).strip() + "\n"

    def _component_lines(self, architecture: ArchitectureModel, language: str) -> list[str]:
        if not architecture.components:
            return [
                "- Nenhum componente foi detectado."
                if language == "pt-BR"
                else "- No components were detected."
            ]

        lines: list[str] = []
        for component in architecture.components:
            if language == "pt-BR":
                lines.extend(
                    [
                        f"### {component.id} - {component.name}",
                        f"- Tipo: {component.type}",
                        f"- Zona: {component.zone or 'desconhecida'}",
                        f"- Exposição: {component.exposure or 'desconhecida'}",
                        f"- Confiança do detector: {component.confidence:.0%}",
                        f"- Requer validação humana: {'sim' if component.needs_human_validation else 'não'}",
                        "",
                    ]
                )
            else:
                lines.extend(
                    [
                        f"### {component.id} - {component.name}",
                        f"- Type: {component.type}",
                        f"- Zone: {component.zone or 'unknown'}",
                        f"- Exposure: {component.exposure or 'unknown'}",
                        f"- Detector confidence: {component.confidence:.0%}",
                        f"- Human validation required: {'yes' if component.needs_human_validation else 'no'}",
                        "",
                    ]
                )
        return lines

    def save_markdown(self, report_markdown: str) -> str:
        report_id = uuid4().hex
        report_dir = settings.resolved_storage_dir / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        Path(report_dir / f"{report_id}.md").write_text(report_markdown, encoding="utf-8")
        return report_id
