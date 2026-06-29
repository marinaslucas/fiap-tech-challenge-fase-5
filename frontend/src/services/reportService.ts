import { postJson } from "./api";
import type { Detection } from "../types/detection";

interface CreateReportResponse {
  report_id: string;
  format: string;
}

export function createReport(detections: Detection[]) {
  return postJson<CreateReportResponse, { detections: Detection[] }>("/reports", { detections });
}
