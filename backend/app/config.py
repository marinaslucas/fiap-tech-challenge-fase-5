from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    app_name: str = "ThreatGraph AI"
    app_env: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins_raw: str = Field(
        "http://localhost:5173,http://127.0.0.1:5173",
        alias="CORS_ORIGINS",
    )
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.1-flash-lite"
    llm_enabled: bool = True
    model_path: Path = Path("models/best.pt")
    model_metadata_path: Path = Path("models/model_metadata.json")
    detector_confidence_threshold: float = Field(0.15, ge=0.0, le=1.0)
    detector_image_size: int = Field(960, ge=32)
    storage_dir: Path = Path("backend/storage")
    frontend_dist_dir_path: Path = Field(Path("frontend/dist"), alias="FRONTEND_DIST_DIR")

    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]

    @property
    def resolved_model_path(self) -> Path:
        return self._resolve_path(self.model_path)

    @property
    def resolved_model_metadata_path(self) -> Path:
        return self._resolve_path(self.model_metadata_path)

    @property
    def resolved_storage_dir(self) -> Path:
        return self._resolve_path(self.storage_dir)

    @property
    def resolved_frontend_dist_dir(self) -> Path:
        return self._resolve_path(self.frontend_dist_dir_path)

    @property
    def frontend_dist_dir(self) -> Path:
        return self.resolved_frontend_dist_dir

    def _resolve_path(self, path: Path) -> Path:
        if path.is_absolute():
            return path
        project_path = PROJECT_ROOT / path
        if project_path.exists() or path.parts[:1] in {("models",), ("backend",)}:
            return project_path
        return BACKEND_ROOT / path


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
