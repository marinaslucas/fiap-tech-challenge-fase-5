import { FileDown } from "lucide-react";

import ComponentOverview from "../components/ComponentOverview";
import DetectionViewer from "../components/DetectionViewer";
import ReportViewer from "../components/ReportViewer";
import RiskMatrix from "../components/RiskMatrix";
import ThreatTable from "../components/ThreatTable";
import type { Detection } from "../types/detection";
import type { AnalysisResponse } from "../types/report";

interface ReportPageProps {
  analysis: AnalysisResponse | null;
  imageUrl: string | null;
  detections: Detection[];
}

export default function ReportPage({ analysis, imageUrl, detections }: ReportPageProps) {
  const isPtBr = analysis?.audit.report_language === "pt-BR";

  function handleExportPdf() {
    window.print();
  }

  return (
    <section className="page-grid">
      <header className="page-header">
        <div>
          <p className="eyebrow">{isPtBr ? "Resultado STRIDE" : "STRIDE Output"}</p>
          <h1>{isPtBr ? "Relat\u00f3rio de Amea\u00e7as" : "Threat Report"}</h1>
        </div>
        {analysis && (
          <button className="primary-action no-print" onClick={handleExportPdf}>
            <FileDown size={18} aria-hidden="true" />
            {isPtBr ? "Exportar PDF" : "Export PDF"}
          </button>
        )}
      </header>

      {analysis ? (
        <>
          <RiskMatrix threats={analysis.threats} />
          <section className="annotated-diagram">
            <div className="panel-title">{isPtBr ? "Diagrama Anotado" : "Annotated Diagram"}</div>
            <div className="annotated-diagram-body">
              <DetectionViewer imageUrl={imageUrl} detections={detections} showFooter={false} />
            </div>
          </section>
          <ComponentOverview components={analysis.architecture.components} language={analysis.audit.report_language} />
          <ThreatTable threats={analysis.threats} language={analysis.audit.report_language} />
          <ReportViewer markdown={analysis.report_markdown} />
        </>
      ) : (
        <div className="empty-state">No report generated yet.</div>
      )}
    </section>
  );
}
