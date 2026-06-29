export interface ArchitectureComponent {
  id: string;
  type: string;
  name: string;
  zone: string | null;
  exposure: string | null;
  confidence: number;
  needs_human_validation: boolean;
}

export interface ArchitectureFlow {
  source: string;
  target: string;
  protocol: string | null;
  confidence: string;
}

export interface ArchitectureModel {
  components: ArchitectureComponent[];
  flows: ArchitectureFlow[];
  trust_boundaries: string[];
}
