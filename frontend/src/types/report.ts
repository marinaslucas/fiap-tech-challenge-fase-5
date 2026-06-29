import type { ArchitectureModel } from "./architecture";
import type { Countermeasure, Threat, VulnerabilityFinding } from "./threat";

export interface AnalysisResponse {
  architecture: ArchitectureModel;
  threats: Threat[];
  vulnerabilities: VulnerabilityFinding[];
  countermeasures: Countermeasure[];
  report_markdown: string;
}
