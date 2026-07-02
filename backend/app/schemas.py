from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    component_type: str
    confidence: float = Field(ge=0, le=1)
    bbox: BoundingBox


class DetectionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    image_id: str
    detections: list[Detection]
    model_version: str = "placeholder"
    needs_human_validation: bool = True


class ArchitectureComponent(BaseModel):
    id: str
    type: str
    name: str
    zone: str | None = None
    exposure: str | None = None
    confidence: float = Field(ge=0, le=1)
    needs_human_validation: bool = True


class ArchitectureFlow(BaseModel):
    source: str
    target: str
    protocol: str | None = None
    confidence: str = "Low"


class ArchitectureModel(BaseModel):
    components: list[ArchitectureComponent]
    flows: list[ArchitectureFlow] = []
    trust_boundaries: list[str] = []


class Threat(BaseModel):
    id: str
    component_id: str
    stride_category: str
    description: str
    severity: str
    confidence: str
    evidence: str
    needs_validation: list[str] = []


class VulnerabilityFinding(BaseModel):
    threat_id: str
    weakness: str
    rationale: str
    confidence: str


class Countermeasure(BaseModel):
    threat_id: str
    recommendation: str
    priority: str


class SecurityReference(BaseModel):
    threat_id: str
    source: str
    reference_id: str
    title: str
    url: str
    note: str


class GeminiConfig(BaseModel):
    api_key: str | None = None
    model: str | None = None
    report_language: Literal["en", "pt-BR"] = "en"


class AnalysisRequest(BaseModel):
    detections: list[Detection]


class AnalysisAudit(BaseModel):
    detector_input_count: int
    normalized_component_count: int
    threat_count: int
    vulnerability_count: int
    countermeasure_count: int
    reference_count: int = 0
    report_language: Literal["en", "pt-BR"]
    gemini_model: str | None = None
    gemini_configured: bool = False
    llm_used: bool = False
    fallback_used: bool = False
    fallback_reason: str | None = None
    stride_prompt: str | None = None
    agent_log: list[str] = []


class AnalysisResponse(BaseModel):
    architecture: ArchitectureModel
    threats: list[Threat]
    vulnerabilities: list[VulnerabilityFinding]
    countermeasures: list[Countermeasure]
    references: list[SecurityReference] = []
    report_markdown: str
    audit: AnalysisAudit
