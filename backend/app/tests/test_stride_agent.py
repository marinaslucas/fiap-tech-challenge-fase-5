from app.agents.stride_agent import StrideAgent
from app.schemas import ArchitectureComponent, ArchitectureFlow, ArchitectureModel


def test_stride_agent_generates_dos_for_internet_facing_component() -> None:
    architecture = ArchitectureModel(
        components=[
            ArchitectureComponent(
                id="component_001",
                type="api_gateway",
                name="API Gateway",
                zone="edge",
                exposure="internet-facing",
                confidence=0.9,
            )
        ]
    )

    threats = StrideAgent().run(architecture)

    assert threats
    assert threats[0].stride_category == "Denial of Service"


def test_stride_prompt_is_evidence_based_and_not_mvp_specific() -> None:
    architecture = ArchitectureModel(
        components=[
            ArchitectureComponent(
                id="component_001",
                type="api_gateway",
                name="API Gateway",
                zone="edge",
                exposure="internet-facing",
                confidence=0.9,
            )
        ]
    )

    prompt = StrideAgent()._build_prompt(architecture, "pt-BR")

    assert "hackathon MVP" not in prompt
    assert "senior cybersecurity architect" in prompt
    assert "Never invent components" in prompt
    assert "absence of a control" in prompt
    assert "Brazilian Portuguese" in prompt
    assert '\"id\": \"component_001\"' in prompt


def test_fallback_generates_distinct_architecture_specific_findings() -> None:
    components = [
        ArchitectureComponent(
            id="component_001",
            type="actor_user",
            name="Actor User",
            zone="internet",
            exposure="external",
            confidence=0.93,
        ),
        ArchitectureComponent(
            id="component_002",
            type="edge_ddos_protection",
            name="Edge Ddos Protection",
            zone="edge",
            exposure="internet-facing",
            confidence=0.99,
        ),
        ArchitectureComponent(
            id="component_003",
            type="compute_load_balancer",
            name="Compute Load Balancer",
            zone="edge",
            exposure="internet-facing",
            confidence=0.98,
        ),
        ArchitectureComponent(
            id="component_004",
            type="compute_load_balancer",
            name="Compute Load Balancer",
            zone="edge",
            exposure="internet-facing",
            confidence=0.96,
        ),
        ArchitectureComponent(
            id="component_005",
            type="data_database",
            name="Data Database",
            zone="data",
            exposure="internal",
            confidence=0.98,
        ),
        ArchitectureComponent(
            id="component_006",
            type="security_key_management",
            name="Security Key Management",
            zone="security",
            exposure="internal",
            confidence=0.97,
        ),
        ArchitectureComponent(
            id="component_007",
            type="obs_audit",
            name="Obs Audit",
            zone="security",
            exposure="internal",
            confidence=0.98,
        ),
        ArchitectureComponent(
            id="component_008",
            type="backup_service",
            name="Backup Service",
            zone="application",
            exposure="internal",
            confidence=0.99,
        ),
    ]
    architecture = ArchitectureModel(
        components=components,
        flows=[
            ArchitectureFlow(
                source="component_001",
                target="component_003",
                protocol="HTTPS",
                confidence="Low",
            )
        ],
    )

    threats = StrideAgent()._run_with_rules(architecture, "en")

    assert [threat.id for threat in threats] == [f"T{index:03d}" for index in range(1, 7)]
    assert {threat.stride_category for threat in threats} == {
        "Denial of Service",
        "Spoofing",
        "Information Disclosure",
        "Elevation of Privilege",
        "Repudiation",
        "Tampering",
    }
    assert all(threat.component_id != "component_002" for threat in threats)
    assert sum(threat.stride_category == "Denial of Service" for threat in threats) == 1
    assert all("detector confidence" in threat.evidence for threat in threats)
    assert all(threat.needs_validation for threat in threats)


class StubLlmService:
    model = "gemini-3.1-flash-lite"
    last_error = None

    def is_enabled(self) -> bool:
        return True

    def generate_json(self, prompt: str) -> dict[str, object]:
        del prompt
        valid = {
            "id": "T999",
            "component_id": "component_001",
            "stride_category": "Denial of Service",
            "description": "A supported finding.",
            "severity": "High",
            "confidence": "Medium",
            "evidence": "Internet-facing API gateway.",
            "needs_validation": ["Confirm rate limits."],
        }
        invalid = {**valid, "id": "T998", "component_id": "invented_component"}
        return {"threats": [invalid, valid, valid]}


def test_llm_findings_are_validated_deduplicated_and_renumbered() -> None:
    architecture = ArchitectureModel(
        components=[
            ArchitectureComponent(
                id="component_001",
                type="api_gateway",
                name="API Gateway",
                zone="edge",
                exposure="internet-facing",
                confidence=0.9,
            )
        ]
    )
    agent = StrideAgent(llm_service=StubLlmService())  # type: ignore[arg-type]

    threats = agent.run(architecture)

    assert len(threats) == 1
    assert threats[0].id == "T001"
    assert threats[0].component_id == "component_001"
    assert agent.audit["llm_used"] is True
