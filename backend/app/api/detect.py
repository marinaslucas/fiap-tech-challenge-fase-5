from fastapi import APIRouter, File, UploadFile

from app.schemas import DetectionResponse
from app.services.detector_service import DetectorService
from app.services.image_service import ImageService

router = APIRouter(prefix="/detect", tags=["detection"])


@router.post("", response_model=DetectionResponse)
async def detect_components(file: UploadFile = File(...)) -> DetectionResponse:
    image = await ImageService().save_upload(file)
    return DetectorService().detect(image.path, image.image_id)
