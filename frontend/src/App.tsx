import { FileText, History, KeyRound, Radar, UploadCloud } from "lucide-react";
import { useState } from "react";

import HistoryPage from "./pages/HistoryPage";
import ReportPage from "./pages/ReportPage";
import ReviewComponentsPage from "./pages/ReviewComponentsPage";
import UploadPage from "./pages/UploadPage";
import type { Detection } from "./types/detection";
import type { AnalysisResponse } from "./types/report";

type Page = "upload" | "review" | "report" | "history";

const GEMINI_MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash"];
const REPORT_LANGUAGES = [
  { value: "en", label: "English" },
  { value: "pt-BR", label: "Português (BR)" },
] as const;

export default function App() {
  const [page, setPage] = useState<Page>("upload");
  const [detections, setDetections] = useState<Detection[]>([]);
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [geminiApiKey, setGeminiApiKey] = useState("");
  const [geminiModel, setGeminiModel] = useState(GEMINI_MODELS[0]);
  const [reportLanguage, setReportLanguage] = useState<"en" | "pt-BR">("en");

  const geminiConfig = {
    apiKey: geminiApiKey.trim() || undefined,
    model: geminiModel,
    reportLanguage,
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Radar size={24} aria-hidden="true" />
          <span>ThreatGraph AI</span>
        </div>
        <nav className="nav-list" aria-label="Primary">
          <button className={page === "upload" ? "active" : ""} onClick={() => setPage("upload")}>
            <UploadCloud size={18} aria-hidden="true" />
            Upload
          </button>
          <button className={page === "review" ? "active" : ""} onClick={() => setPage("review")}>
            <Radar size={18} aria-hidden="true" />
            Review
          </button>
          <button className={page === "report" ? "active" : ""} onClick={() => setPage("report")}>
            <FileText size={18} aria-hidden="true" />
            Report
          </button>
          <button className={page === "history" ? "active" : ""} onClick={() => setPage("history")}>
            <History size={18} aria-hidden="true" />
            History
          </button>
        </nav>
        <section className="gemini-panel" aria-label="Gemini settings">
          <div className="gemini-title">
            <KeyRound size={16} aria-hidden="true" />
            <span>Gemini</span>
          </div>
          <label>
            <span>API key</span>
            <input
              autoComplete="off"
              spellCheck={false}
              type="password"
              value={geminiApiKey}
              placeholder="AIza..."
              onChange={(event) => setGeminiApiKey(event.target.value)}
            />
          </label>
          <label>
            <span>Model</span>
            <select value={geminiModel} onChange={(event) => setGeminiModel(event.target.value)}>
              {GEMINI_MODELS.map((model) => (
                <option key={model} value={model}>
                  {model}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span>Report language</span>
            <select
              value={reportLanguage}
              onChange={(event) => setReportLanguage(event.target.value as "en" | "pt-BR")}
            >
              {REPORT_LANGUAGES.map((language) => (
                <option key={language.value} value={language.value}>
                  {language.label}
                </option>
              ))}
            </select>
          </label>
          <button className="secondary-action" type="button" onClick={() => setGeminiApiKey("")}>
            Clear key
          </button>
        </section>
      </aside>

      <main className="workspace">
        {page === "upload" && (
          <UploadPage
            imageUrl={imageUrl}
            detections={detections}
            onImageSelected={setImageUrl}
            onDetections={setDetections}
            onAnalysis={(result) => {
              setAnalysis(result);
              setPage("report");
            }}
            geminiConfig={geminiConfig}
          />
        )}
        {page === "review" && (
          <ReviewComponentsPage
            detections={detections}
            onAnalyze={(result) => {
              setAnalysis(result);
              setPage("report");
            }}
            geminiConfig={geminiConfig}
          />
        )}
        {page === "report" && <ReportPage analysis={analysis} />}
        {page === "history" && <HistoryPage />}
      </main>
    </div>
  );
}
