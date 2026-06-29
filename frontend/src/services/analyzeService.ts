import { type GeminiRequestConfig, postJson } from "./api";
import type { Detection } from "../types/detection";
import type { AnalysisResponse } from "../types/report";

export function analyzeDetections(detections: Detection[], geminiConfig?: GeminiRequestConfig) {
  return postJson<AnalysisResponse, { detections: Detection[] }>(
    "/analyze",
    { detections },
    geminiConfig,
  );
}
