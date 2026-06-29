from app.schemas import ArchitectureModel, Detection
from app.services.topology_service import TopologyService


class TopologyAgent:
    def __init__(self, topology_service: TopologyService | None = None) -> None:
        self.topology_service = topology_service or TopologyService()

    def run(self, detections: list[Detection]) -> ArchitectureModel:
        return self.topology_service.normalize(detections)
