from fastapi import APIRouter

from app.graph import run_analysis_graph
from app.schemas import AnalysisRequest
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("")
def create_report(payload: AnalysisRequest) -> dict[str, str]:
    analysis = run_analysis_graph(payload.detections)
    report_id = ReportService().save_markdown(analysis.report_markdown)
    return {"report_id": report_id, "format": "markdown"}
