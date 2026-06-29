import { Loader2, ShieldCheck } from "lucide-react";
import { useState } from "react";

import ComponentTable from "../components/ComponentTable";
import { analyzeDetections } from "../services/analyzeService";
import type { GeminiRequestConfig } from "../services/api";
import type { Detection } from "../types/detection";
import type { AnalysisResponse } from "../types/report";

interface ReviewComponentsPageProps {
  detections: Detection[];
  onAnalyze: (analysis: AnalysisResponse) => void;
  geminiConfig: GeminiRequestConfig;
}

export default function ReviewComponentsPage({
  detections,
  onAnalyze,
  geminiConfig,
}: ReviewComponentsPageProps) {
  const [isBusy, setIsBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyze() {
    setIsBusy(true);
    setError(null);

    try {
      onAnalyze(await analyzeDetections(detections, geminiConfig));
    } catch {
      setError("Analysis failed. Check the backend logs and Gemini API key configuration.");
    } finally {
      setIsBusy(false);
    }
  }

  return (
    <section className="page-grid">
      <header className="page-header">
        <div>
          <p className="eyebrow">Component Review</p>
          <h1>Detected Components</h1>
        </div>
        <button className="primary-action" disabled={!detections.length || isBusy} onClick={handleAnalyze}>
          {isBusy ? <Loader2 className="spin" size={18} aria-hidden="true" /> : <ShieldCheck size={18} aria-hidden="true" />}
          {isBusy ? "Working..." : "Analyze"}
        </button>
      </header>
      <div className="status-strip" aria-live="polite">
        {isBusy && <Loader2 className="spin" size={16} aria-hidden="true" />}
        <span>
          {isBusy
            ? "Generating STRIDE analysis..."
            : detections.length
              ? "Components are ready for analysis."
              : "No detected components to review yet."}
        </span>
      </div>
      {error && <div className="inline-error">{error}</div>}
      <ComponentTable detections={detections} isBusy={isBusy} />
    </section>
  );
}
