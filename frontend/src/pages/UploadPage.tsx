import { Loader2, ShieldCheck } from "lucide-react";
import { useState } from "react";

import ComponentTable from "../components/ComponentTable";
import DetectionViewer from "../components/DetectionViewer";
import ImageUploader from "../components/ImageUploader";
import { analyzeDetections } from "../services/analyzeService";
import type { GeminiRequestConfig } from "../services/api";
import { detectComponents } from "../services/api";
import type { Detection } from "../types/detection";
import type { AnalysisResponse } from "../types/report";
import { prepareImageForDetection } from "../utils/image";

interface UploadPageProps {
  imageUrl: string | null;
  detections: Detection[];
  onImageSelected: (imageUrl: string) => void;
  onDetections: (detections: Detection[]) => void;
  onAnalysis: (analysis: AnalysisResponse) => void;
  geminiConfig: GeminiRequestConfig;
}

export default function UploadPage({
  imageUrl,
  detections,
  onImageSelected,
  onDetections,
  onAnalysis,
  geminiConfig,
}: UploadPageProps) {
  const [isBusy, setIsBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("Upload a diagram to start detection.");

  async function handleFile(file: File) {
    setIsBusy(true);
    setError(null);
    onDetections([]);
    setStatus(file.name.toLowerCase().endsWith(".svg") ? "Converting SVG to PNG..." : "Preparing image...");

    try {
      const detectionFile = await prepareImageForDetection(file);
      onImageSelected(URL.createObjectURL(detectionFile));
      setStatus("Running component detector...");
      const response = await detectComponents(detectionFile);
      onDetections(response.detections);
      setStatus(
        response.detections.length
          ? `${response.detections.length} component${response.detections.length === 1 ? "" : "s"} detected.`
          : "No components detected. You can still analyze the uploaded diagram context.",
      );
    } catch (error) {
      setError(error instanceof Error ? error.message : "Detection failed.");
      setStatus("Detection stopped.");
      onDetections([]);
    } finally {
      setIsBusy(false);
    }
  }

  async function handleAnalyze() {
    setIsBusy(true);
    setError(null);
    setStatus("Generating STRIDE analysis...");

    try {
      onAnalysis(await analyzeDetections(detections, geminiConfig));
    } catch {
      setError("Analysis failed. Check the backend logs and Gemini API key configuration.");
      setStatus("Analysis stopped.");
    } finally {
      setIsBusy(false);
    }
  }

  const canAnalyze = Boolean(imageUrl) && !isBusy;

  return (
    <section className="page-grid">
      <header className="page-header">
        <div>
          <p className="eyebrow">Architecture Intake</p>
          <h1>Diagram Analysis</h1>
        </div>
        <button className="primary-action" disabled={!canAnalyze} onClick={handleAnalyze}>
          {isBusy ? <Loader2 className="spin" size={18} aria-hidden="true" /> : <ShieldCheck size={18} aria-hidden="true" />}
          {isBusy ? "Working..." : "Analyze"}
        </button>
      </header>

      <div className="two-column">
        <div className="panel">
          <ImageUploader disabled={isBusy} onFile={handleFile} />
          <div className="status-strip" aria-live="polite">
            {isBusy && <Loader2 className="spin" size={16} aria-hidden="true" />}
            <span>{status}</span>
          </div>
          {error && <div className="inline-error">{error}</div>}
          <DetectionViewer imageUrl={imageUrl} detections={detections} isBusy={isBusy} />
        </div>
        <ComponentTable detections={detections} isBusy={isBusy} />
      </div>
    </section>
  );
}
