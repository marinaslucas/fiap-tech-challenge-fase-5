from fastapi import APIRouter, Header

from app.graph import run_analysis_graph
from app.schemas import AnalysisRequest, AnalysisResponse, GeminiConfig

router = APIRouter(prefix="/analyze", tags=["analysis"])


@router.post("", response_model=AnalysisResponse)
def analyze_architecture(
    payload: AnalysisRequest,
    x_gemini_api_key: str | None = Header(default=None, alias="X-Gemini-Api-Key"),
    x_gemini_model: str | None = Header(default=None, alias="X-Gemini-Model"),
    x_report_language: str | None = Header(default=None, alias="X-Report-Language"),
) -> AnalysisResponse:
    gemini_config = GeminiConfig(
        api_key=x_gemini_api_key,
        model=x_gemini_model,
        report_language="pt-BR" if x_report_language == "pt-BR" else "en",
    )

    return run_analysis_graph(payload.detections, gemini_config=gemini_config)
