from app.agents.stride_agent import StrideAgent
from app.schemas import ArchitectureComponent, ArchitectureModel


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
