from app.agents.countermeasure_agent import CountermeasureAgent
from app.agents.reference_agent import ReferenceAgent
from app.agents.report_agent import ReportAgent
from app.agents.stride_agent import StrideAgent
from app.agents.topology_agent import TopologyAgent
from app.agents.vulnerability_agent import VulnerabilityAgent
from app.schemas import AnalysisAudit, AnalysisResponse, Detection, GeminiConfig


def run_analysis_graph(
    detections: list[Detection],
    gemini_config: GeminiConfig | None = None,
) -> AnalysisResponse:
    topology_agent = TopologyAgent()
    stride_agent = StrideAgent()
    vulnerability_agent = VulnerabilityAgent()
    countermeasure_agent = CountermeasureAgent()
    reference_agent = ReferenceAgent()
    report_agent = ReportAgent()
    report_language = gemini_config.report_language if gemini_config else "en"

    architecture = topology_agent.run(detections)
    threats = stride_agent.run(architecture, gemini_config=gemini_config)
    vulnerabilities = vulnerability_agent.run(threats, report_language=report_language)
    countermeasures = countermeasure_agent.run(threats, report_language=report_language)
    references = reference_agent.run(threats, report_language=report_language)
    report_markdown = report_agent.run(
        architecture=architecture,
        threats=threats,
        vulnerabilities=vulnerabilities,
        countermeasures=countermeasures,
        references=references,
        report_language=report_language,
    )
    stride_audit = stride_agent.audit

    return AnalysisResponse(
        architecture=architecture,
        threats=threats,
        vulnerabilities=vulnerabilities,
        countermeasures=countermeasures,
        references=references,
        report_markdown=report_markdown,
        audit=AnalysisAudit(
            detector_input_count=len(detections),
            normalized_component_count=len(architecture.components),
            threat_count=len(threats),
            vulnerability_count=len(vulnerabilities),
            countermeasure_count=len(countermeasures),
            reference_count=len(references),
            report_language=report_language,
            gemini_model=stride_audit.get("model") if stride_audit else None,
            gemini_configured=bool(stride_audit.get("gemini_configured")) if stride_audit else False,
            llm_used=bool(stride_audit.get("llm_used")) if stride_audit else False,
            fallback_used=bool(stride_audit.get("fallback_used")) if stride_audit else False,
            fallback_reason=stride_audit.get("fallback_reason") if stride_audit else None,
            stride_prompt=stride_audit.get("prompt") if stride_audit else None,
            agent_log=[
                f"TopologyAgent normalized {len(detections)} detections into {len(architecture.components)} components.",
                f"STRIDEAgent generated {len(threats)} threats using {'Gemini' if stride_audit.get('llm_used') else 'local fallback rules'}.",
                f"VulnerabilityAgent mapped {len(vulnerabilities)} vulnerability findings.",
                f"CountermeasureAgent generated {len(countermeasures)} countermeasures.",
                f"ReferenceAgent attached {len(references)} curated CWE, OWASP, NIST, and CVE validation references.",
                "ReportAgent rendered the final report markdown.",
            ],
        ),
    )
