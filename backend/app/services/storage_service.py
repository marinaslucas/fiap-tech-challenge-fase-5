from pathlib import Path
from uuid import uuid4

from app.config import settings


class StorageService:
    def write_text(self, folder: str, content: str, suffix: str = ".txt") -> Path:
        target_dir = settings.resolved_storage_dir / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{uuid4().hex}{suffix}"
        path.write_text(content, encoding="utf-8")
        return path
