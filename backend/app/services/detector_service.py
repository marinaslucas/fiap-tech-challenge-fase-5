import json
from pathlib import Path

from fastapi import HTTPException

from app.config import settings
from app.schemas import BoundingBox, Detection, DetectionResponse

SUPPORTED_IMAGE_SUFFIXES = {
    ".avif",
    ".bmp",
    ".dng",
    ".heic",
    ".heif",
    ".jpeg",
    ".jpeg2000",
    ".jpg",
    ".jp2",
    ".mpo",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


class DetectorService:
    _model = None
    _metadata: dict | None = None

    def detect(self, image_path: Path, image_id: str) -> DetectionResponse:
        if image_path.suffix.lower() not in SUPPORTED_IMAGE_SUFFIXES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Formato de imagem não suportado pelo detector. "
                    "Envie PNG, JPG ou WebP. SVG deve ser convertido para PNG."
                ),
            )

        model_path = settings.resolved_model_path
        if not model_path.exists():
            return DetectionResponse(
                image_id=image_id,
                detections=[],
                model_version="model-not-found",
                needs_human_validation=True,
            )

        model = self._load_model(model_path)
        results = model.predict(
            source=str(image_path),
            conf=settings.detector_confidence_threshold,
            imgsz=settings.detector_image_size,
            iou=0.7,
            max_det=300,
            verbose=False,
        )
        detections = self._to_detections(results[0])

        return DetectionResponse(
            image_id=image_id,
            detections=detections,
            model_version=self._model_version(model_path),
            needs_human_validation=any(item.confidence < 0.8 for item in detections),
        )

    def _load_model(self, model_path: Path):
        if self.__class__._model is None:
            from ultralytics import YOLO

            self.__class__._model = YOLO(str(model_path))
        return self.__class__._model

    def _to_detections(self, result) -> list[Detection]:
        detections: list[Detection] = []
        names = result.names

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            x1, y1, x2, y2 = [float(value) for value in box.xyxy[0].tolist()]
            detections.append(
                Detection(
                    component_type=names[class_id],
                    confidence=round(confidence, 4),
                    bbox=BoundingBox(
                        x1=round(x1, 2),
                        y1=round(y1, 2),
                        x2=round(x2, 2),
                        y2=round(y2, 2),
                    ),
                )
            )

        return detections

    def _model_version(self, model_path: Path) -> str:
        metadata = self._load_metadata()
        return str(metadata.get("run_name") or metadata.get("model_name") or model_path.name)

    def _load_metadata(self) -> dict:
        if self.__class__._metadata is not None:
            return self.__class__._metadata

        metadata_path = settings.resolved_model_metadata_path
        if not metadata_path.exists():
            self.__class__._metadata = {}
            return self.__class__._metadata

        self.__class__._metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        return self.__class__._metadata
