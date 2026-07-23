from types import SimpleNamespace

from app.services.detector_service import DetectorService


class _Scalar:
    def __init__(self, value: float) -> None:
        self.value = value

    def item(self) -> float:
        return self.value


class _Vector:
    def __init__(self, values: list[float]) -> None:
        self.values = values

    def tolist(self) -> list[float]:
        return self.values


def _box(class_id: int, confidence: float) -> SimpleNamespace:
    return SimpleNamespace(
        cls=[_Scalar(class_id)],
        conf=[_Scalar(confidence)],
        xyxy=[_Vector([1.0, 2.0, 30.0, 40.0])],
    )


def test_to_detections_filters_diagnostic_candidates_below_threshold() -> None:
    result = SimpleNamespace(
        names={0: "edge_gateway", 1: "data_storage"},
        boxes=[_box(0, 0.42), _box(1, 0.08)],
    )

    detections = DetectorService()._to_detections(result, min_confidence=0.15)

    assert len(detections) == 1
    assert detections[0].component_type == "edge_gateway"
    assert detections[0].confidence == 0.42
