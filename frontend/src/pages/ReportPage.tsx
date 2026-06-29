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
  const labels = isPtBr
    ? {
        eyebrow: "Resultado STRIDE",
        title: "Relat\u00f3rio de Amea\u00e7as",
        exportPdf: "Exportar PDF",
        generatedAt: "Gerado em",
        status: "Status",
        critical: "Cr\u00edticas",
        high: "Altas",
        medium: "M\u00e9dias",
        components: "Componentes",
        flows: "Fluxos inferidos",
        threats: "Amea\u00e7as",
        validation: "Valida\u00e7\u00e3o humana recomendada",
        needsReview: "Revis\u00e3o necess\u00e1ria",
        stable: "Baixo risco imediato",
        attention: "Aten\u00e7\u00e3o requerida",
        criticalStatus: "Prioridade cr\u00edtica",
        annotatedDiagram: "Diagrama Anotado",
        noReport: "Nenhum relat\u00f3rio gerado ainda.",
      }
    : {
        eyebrow: "STRIDE Output",
        title: "Threat Report",
        exportPdf: "Export PDF",
        generatedAt: "Generated at",
        status: "Status",
        critical: "Critical",
        high: "High",
        medium: "Medium",
        components: "Components",
        flows: "Inferred flows",
        threats: "Threats",
        validation: "Human validation recommended",
        needsReview: "Review needed",
        stable: "Low immediate risk",
        attention: "Attention required",
        criticalStatus: "Critical priority",
        annotatedDiagram: "Annotated Diagram",
        noReport: "No report generated yet.",
      };
  const generatedAt = new Intl.DateTimeFormat(isPtBr ? "pt-BR" : "en-US", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date());
  const severityCount = (severity: string) =>
    analysis?.threats.filter((threat) => threat.severity === severity).length ?? 0;
  const criticalCount = severityCount("Critical");
  const highCount = severityCount("High");
  const mediumCount = severityCount("Medium");
  const reportStatus =
    criticalCount > 0
      ? { label: labels.criticalStatus, className: "critical" }
      : highCount > 0 || mediumCount > 0
        ? { label: labels.attention, className: "attention" }
        : { label: labels.stable, className: "stable" };

  function handleExportPdf() {
    window.print();
  }

  return (
    <section className="page-grid">
      <header className="page-header">
        <div>
          <p className="eyebrow">{labels.eyebrow}</p>
          <h1>{labels.title}</h1>
        </div>
        {analysis && (
          <button className="primary-action no-print" onClick={handleExportPdf}>
            <FileDown size={18} aria-hidden="true" />
            {labels.exportPdf}
          </button>
        )}
      </header>

      {analysis ? (
        <article className="report-print-shell">
          <header className="report-document-header">
            <div>
              <p className="eyebrow">ThreatGraph AI</p>
              <h2>{labels.title}</h2>
            </div>
            <dl className="report-document-meta">
              <div>
                <dt>{labels.generatedAt}</dt>
                <dd>{generatedAt}</dd>
              </div>
              <div>
                <dt>Language</dt>
                <dd>{analysis.audit.report_language}</dd>
              </div>
            </dl>
          </header>

          <section className={`report-summary-card ${reportStatus.className}`}>
            <div>
              <span>{labels.status}</span>
              <strong>{reportStatus.label}</strong>
              <p>{labels.validation}</p>
            </div>
            <dl className="report-summary-kpis">
              <div>
                <dt>{labels.critical}</dt>
                <dd>{criticalCount}</dd>
              </div>
              <div>
                <dt>{labels.high}</dt>
                <dd>{highCount}</dd>
              </div>
              <div>
                <dt>{labels.medium}</dt>
                <dd>{mediumCount}</dd>
              </div>
              <div>
                <dt>{labels.components}</dt>
                <dd>{analysis.architecture.components.length}</dd>
              </div>
              <div>
                <dt>{labels.flows}</dt>
                <dd>{analysis.architecture.flows.length}</dd>
              </div>
              <div>
                <dt>{labels.threats}</dt>
                <dd>{analysis.threats.length}</dd>
              </div>
            </dl>
          </section>

          <RiskMatrix threats={analysis.threats} />
          <section className="annotated-diagram">
            <div className="panel-title">{labels.annotatedDiagram}</div>
            <div className="annotated-diagram-body">
              <DetectionViewer imageUrl={imageUrl} detections={detections} showFooter={false} />
            </div>
          </section>
          <ComponentOverview components={analysis.architecture.components} language={analysis.audit.report_language} />
          <ThreatTable threats={analysis.threats} language={analysis.audit.report_language} />
          <ReportViewer markdown={analysis.report_markdown} />
          <footer className="report-print-footer">
            ThreatGraph AI - STRIDE Report
          </footer>
        </article>
      ) : (
        <div className="empty-state">{labels.noReport}</div>
      )}
    </section>
  );
}
