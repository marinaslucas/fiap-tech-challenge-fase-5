export interface Threat {
  id: string;
  component_id: string;
  stride_category: string;
  description: string;
  severity: string;
  confidence: string;
  evidence: string;
  needs_validation: string[];
}

export interface VulnerabilityFinding {
  threat_id: string;
  weakness: string;
  rationale: string;
  confidence: string;
}

export interface Countermeasure {
  threat_id: string;
  recommendation: string;
  priority: string;
}
