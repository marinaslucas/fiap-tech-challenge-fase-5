from app.agents.reference_agent import ReferenceAgent
from app.schemas import Threat


def test_reference_agent_maps_dos_to_curated_sources() -> None:
    threat = Threat(
        id="T001",
        component_id="component_001",
        stride_category="Denial of Service",
        description="Public entry point may be abused.",
        severity="High",
        confidence="Medium",
        evidence="Internet-facing edge gateway.",
    )

    references = ReferenceAgent().run([threat], report_language="en")

    assert {reference.source for reference in references} == {
        "CWE",
        "OWASP API Security",
        "NIST CSF",
    }
    assert any(reference.reference_id == "CWE-400" for reference in references)
    assert any(reference.reference_id == "API4:2023" for reference in references)
    assert all(reference.source != "CVE/NVD" for reference in references)


def test_reference_agent_localizes_pt_br_notes() -> None:
    threat = Threat(
        id="T001",
        component_id="component_001",
        stride_category="Spoofing",
        description="Identidade precisa de validacao.",
        severity="High",
        confidence="Medium",
        evidence="Gateway exposto.",
    )

    references = ReferenceAgent().run([threat], report_language="pt-BR")

    assert references
    assert "autenticacao" in references[0].note
