from app.schemas import BoundingBox, Detection
from app.services.topology_service import TopologyService


def test_normalize_marks_api_gateway_as_internet_facing() -> None:
    detections = [
        Detection(
            component_type="api_gateway",
            confidence=0.91,
            bbox=BoundingBox(x1=0, y1=0, x2=10, y2=10),
        )
    ]

    architecture = TopologyService().normalize(detections)

    assert architecture.components[0].exposure == "internet-facing"
    assert architecture.components[0].confidence == 0.91


def test_normalize_infers_external_actor_to_entrypoint_flow() -> None:
    detections = [
        Detection(
            component_type="actor_user",
            confidence=0.91,
            bbox=BoundingBox(x1=0, y1=0, x2=10, y2=10),
        ),
        Detection(
            component_type="edge_gateway",
            confidence=0.95,
            bbox=BoundingBox(x1=20, y1=0, x2=30, y2=10),
        ),
    ]

    architecture = TopologyService().normalize(detections)

    assert len(architecture.flows) == 1
    assert architecture.flows[0].source == "component_001"
    assert architecture.flows[0].target == "component_002"
    assert architecture.flows[0].protocol == "HTTPS"
    assert architecture.flows[0].confidence == "Low"
