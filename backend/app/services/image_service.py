from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.config import settings


@dataclass(frozen=True)
class SavedImage:
    image_id: str
    path: Path


class ImageService:
    async def save_upload(self, file: UploadFile) -> SavedImage:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Upload must be an image.")

        image_id = uuid4().hex
        suffix = Path(file.filename or "upload.png").suffix or ".png"
        upload_dir = settings.resolved_storage_dir / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)

        destination = upload_dir / f"{image_id}{suffix}"
        destination.write_bytes(await file.read())
        return SavedImage(image_id=image_id, path=destination)
