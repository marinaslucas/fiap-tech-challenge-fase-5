import json
import logging
from pathlib import Path

from fastapi import HTTPException

from app.config import settings
from app.schemas import BoundingBox, Detection, DetectionResponse

logger = logging.getLogger(__name__)

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
            logger.warning("detector_model_not_found model_path=%s", model_path)
            return DetectionResponse(
                image_id=image_id,
                detections=[],
                model_version="model-not-found",
                needs_human_validation=True,
            )

        model = self._load_model(model_path)
        candidate_threshold = min(
            settings.detector_confidence_threshold,
            settings.detector_diagnostic_confidence_threshold,
        )
        results = model.predict(
            source=str(image_path),
            conf=candidate_threshold,
            imgsz=settings.detector_image_size,
            iou=0.7,
            max_det=300,
            verbose=False,
        )
        result = results[0]
        detections = self._to_detections(
            result,
            min_confidence=settings.detector_confidence_threshold,
        )
        self._log_diagnostics(
            result=result,
            image_id=image_id,
            candidate_threshold=candidate_threshold,
            detections=detections,
        )

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

    def _to_detections(self, result, min_confidence: float = 0.0) -> list[Detection]:
        detections: list[Detection] = []
        names = result.names

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            if confidence < min_confidence:
                continue
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

    def _log_diagnostics(
        self,
        result,
        image_id: str,
        candidate_threshold: float,
        detections: list[Detection],
    ) -> None:
        height, width = result.orig_shape
        top_candidates = []
        for box in list(result.boxes)[:10]:
            class_id = int(box.cls[0].item())
            top_candidates.append(
                {
                    "component_type": result.names[class_id],
                    "confidence": round(float(box.conf[0].item()), 4),
                }
            )

        logger.info(
            "detector_diagnostics %s",
            json.dumps(
                {
                    "image_id": image_id,
                    "image_width": width,
                    "image_height": height,
                    "image_size": settings.detector_image_size,
                    "candidate_threshold": candidate_threshold,
                    "detection_threshold": settings.detector_confidence_threshold,
                    "candidate_count": len(result.boxes),
                    "detection_count": len(detections),
                    "top_candidates": top_candidates,
                },
                ensure_ascii=True,
            ),
        )

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
