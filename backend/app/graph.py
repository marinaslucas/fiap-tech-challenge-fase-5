from app.agents.countermeasure_agent import CountermeasureAgent
from app.agents.report_agent import ReportAgent
from app.agents.stride_agent import StrideAgent
from app.agents.topology_agent import TopologyAgent
from app.agents.vulnerability_agent import VulnerabilityAgent
from app.schemas import AnalysisResponse, Detection, GeminiConfig


def run_analysis_graph(
    detections: list[Detection],
    gemini_config: GeminiConfig | None = None,
) -> AnalysisResponse:
    topology_agent = TopologyAgent()
    stride_agent = StrideAgent()
    vulnerability_agent = VulnerabilityAgent()
    countermeasure_agent = CountermeasureAgent()
    report_agent = ReportAgent()

    architecture = topology_agent.run(detections)
    threats = stride_agent.run(architecture, gemini_config=gemini_config)
    vulnerabilities = vulnerability_agent.run(threats)
    countermeasures = countermeasure_agent.run(threats)
    report_markdown = report_agent.run(
        architecture=architecture,
        threats=threats,
        vulnerabilities=vulnerabilities,
        countermeasures=countermeasures,
        report_language=gemini_config.report_language if gemini_config else "en",
    )

    return AnalysisResponse(
        architecture=architecture,
        threats=threats,
        vulnerabilities=vulnerabilities,
        countermeasures=countermeasures,
        report_markdown=report_markdown,
    )
