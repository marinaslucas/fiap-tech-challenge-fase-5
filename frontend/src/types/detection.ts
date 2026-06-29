export interface BoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface Detection {
  component_type: string;
  confidence: number;
  bbox: BoundingBox;
}

export interface DetectionResponse {
  image_id: string;
  detections: Detection[];
  model_version: string;
  needs_human_validation: boolean;
}
