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
