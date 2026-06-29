import json

from app.schemas import ArchitectureModel, GeminiConfig, Threat
from app.services.llm_service import LlmService


class StrideAgent:
    def __init__(self, llm_service: LlmService | None = None) -> None:
        self.llm_service = llm_service or LlmService()
        self.audit: dict[str, object] = {}

    def run(self, architecture: ArchitectureModel, gemini_config: GeminiConfig | None = None) -> list[Threat]:
        report_language = gemini_config.report_language if gemini_config else "en"
        if gemini_config:
            self.llm_service = LlmService(
                api_key=gemini_config.api_key,
                model=gemini_config.model,
            )
        prompt = self._build_prompt(architecture, report_language)
        llm_threats = self._run_with_llm(prompt)
        if llm_threats:
            self.audit = {
                "llm_used": True,
                "fallback_used": False,
                "fallback_reason": None,
                "model": self.llm_service.model,
                "gemini_configured": self.llm_service.is_enabled(),
                "prompt": prompt,
            }
            return llm_threats

        threats = self._run_with_rules(architecture, report_language)
        self.audit = {
            "llm_used": False,
            "fallback_used": True,
            "fallback_reason": self.llm_service.last_error or "Gemini returned no usable threats.",
            "model": self.llm_service.model,
            "gemini_configured": self.llm_service.is_enabled(),
            "prompt": prompt,
        }
        return threats

    def _run_with_llm(self, prompt: str) -> list[Threat]:
        payload = self.llm_service.generate_json(prompt)
        if not payload:
            return []

        threats: list[Threat] = []
        for item in payload.get("threats", []):
            try:
                threats.append(Threat.model_validate(item))
            except Exception:
                continue

        return threats

    def _run_with_rules(self, architecture: ArchitectureModel, report_language: str) -> list[Threat]:
        threats: list[Threat] = []

        for index, component in enumerate(architecture.components, start=1):
            if component.exposure == "internet-facing":
                is_pt = report_language == "pt-BR"
                threats.append(
                    Threat(
                        id=f"T{index:03d}",
                        component_id=component.id,
                        stride_category="Denial of Service",
                        description=(
                            f"{component.name} parece exposto à internet e pode receber tráfego abusivo sem rate limiting."
                            if is_pt
                            else f"{component.name} appears internet-facing and may be exposed to abusive traffic without rate limiting."
                        ),
                        severity="High",
                        confidence="Medium",
                        evidence=(
                            f"Tipo de componente detectado: {component.type}."
                            if is_pt
                            else f"Detected component type: {component.type}."
                        ),
                        needs_validation=[
                            "Confirmar configuração de rate limiting."
                            if is_pt
                            else "Confirm rate limiting configuration.",
                            "Confirmar status de WAF ou proteção de borda."
                            if is_pt
                            else "Confirm WAF or edge protection status.",
                        ],
                    )
                )

        return threats

    def _build_prompt(self, architecture: ArchitectureModel, report_language: str) -> str:
        architecture_json = architecture.model_dump_json(indent=2)
        language_instruction = (
            "Write all user-facing descriptions, evidence and validation questions in Brazilian Portuguese."
            if report_language == "pt-BR"
            else "Write all user-facing descriptions, evidence and validation questions in English."
        )
        return f"""
You are a cybersecurity threat modeling assistant for a hackathon MVP.

Use STRIDE to identify potential risks from the architecture JSON below.
Return only valid JSON. Do not include markdown.

Rules:
- Use the exact JSON shape: {{"threats": [{{...}}]}}.
- Every threat must map to one STRIDE category.
- Every threat must include evidence from the architecture JSON.
- Be careful: diagram-derived findings are potential risks, not confirmed vulnerabilities.
- Prefer 3 to 8 high-signal threats to preserve Gemini free-tier usage.
- {language_instruction}
- Keep STRIDE category, severity and confidence enum values in English.

Each threat object must contain:
- id: T001, T002, ...
- component_id
- stride_category: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, or Elevation of Privilege
- description
- severity: Low, Medium, High, or Critical
- confidence: Low, Medium, or High
- evidence
- needs_validation: array of validation questions

Architecture JSON:
{architecture_json}
""".strip()
