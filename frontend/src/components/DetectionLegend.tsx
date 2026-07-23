import type { Detection } from "../types/detection";

interface DetectionLegendProps {
  detections: Detection[];
  language?: "en" | "pt-BR";
}

export default function DetectionLegend({ detections, language = "en" }: DetectionLegendProps) {
  return (
    <section className="detection-legend print-only">
      <h3>{language === "pt-BR" ? "Legenda das detecções" : "Detection legend"}</h3>
      <ol>
        {detections.map((detection, index) => (
          <li key={`${detection.component_type}-${index}`}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <strong>{detection.component_type.replace(/_/g, " ")}</strong>
            <small>{Math.round(detection.confidence * 100)}%</small>
          </li>
        ))}
      </ol>
    </section>
  );
}
