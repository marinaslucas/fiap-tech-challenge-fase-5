import type { DetectionResponse } from "../types/detection";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  (window.location.port === "5173"
    ? `${window.location.protocol}//${window.location.hostname}:8000`
    : window.location.origin);

export interface GeminiRequestConfig {
  apiKey?: string;
  model?: string;
  reportLanguage?: "en" | "pt-BR";
}

export async function detectComponents(file: File): Promise<DetectionResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/detect`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await errorMessage(response, "Detection request failed."));
  }

  return response.json();
}

export async function postJson<TResponse, TPayload>(
  path: string,
  payload: TPayload,
  geminiConfig?: GeminiRequestConfig,
): Promise<TResponse> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (geminiConfig?.apiKey) {
    headers["X-Gemini-Api-Key"] = geminiConfig.apiKey;
  }

  if (geminiConfig?.model) {
    headers["X-Gemini-Model"] = geminiConfig.model;
  }

  if (geminiConfig?.reportLanguage) {
    headers["X-Report-Language"] = geminiConfig.reportLanguage;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await errorMessage(response, `Request failed: ${path}`));
  }

  return response.json();
}

async function errorMessage(response: Response, fallback: string): Promise<string> {
  try {
    const payload = await response.json();
    if (typeof payload.detail === "string") {
      return payload.detail;
    }
  } catch {
    return fallback;
  }

  return fallback;
}
