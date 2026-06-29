from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, object]:
    return {
        "status": "ok",
        "gemini_configured": bool(settings.gemini_api_key),
        "model_available": settings.resolved_model_path.exists(),
        "model_path": str(settings.resolved_model_path),
    }
