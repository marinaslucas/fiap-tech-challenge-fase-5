import type { ArchitectureModel } from "./architecture";
import type { Countermeasure, SecurityReference, Threat, VulnerabilityFinding } from "./threat";

export interface AnalysisResponse {
  architecture: ArchitectureModel;
  threats: Threat[];
  vulnerabilities: VulnerabilityFinding[];
  countermeasures: Countermeasure[];
  references: SecurityReference[];
  report_markdown: string;
  audit: AnalysisAudit;
}

export interface AnalysisAudit {
  detector_input_count: number;
  normalized_component_count: number;
  threat_count: number;
  vulnerability_count: number;
  countermeasure_count: number;
  reference_count: number;
  report_language: "en" | "pt-BR";
  gemini_model: string | null;
  gemini_configured: boolean;
  llm_used: boolean;
  fallback_used: boolean;
  fallback_reason: string | null;
  stride_prompt: string | null;
  agent_log: string[];
}
