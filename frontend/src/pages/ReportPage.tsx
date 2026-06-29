import { FileDown } from "lucide-react";

import ComponentOverview from "../components/ComponentOverview";
import ReportViewer from "../components/ReportViewer";
import RiskMatrix from "../components/RiskMatrix";
import ThreatTable from "../components/ThreatTable";
import type { AnalysisResponse } from "../types/report";

interface ReportPageProps {
  analysis: AnalysisResponse | null;
}

export default function ReportPage({ analysis }: ReportPageProps) {
  function handleExportPdf() {
    window.print();
  }

  return (
    <section className="page-grid">
      <header className="page-header">
        <div>
          <p className="eyebrow">STRIDE Output</p>
          <h1>Threat Report</h1>
        </div>
        {analysis && (
          <button className="primary-action no-print" onClick={handleExportPdf}>
            <FileDown size={18} aria-hidden="true" />
            Export PDF
          </button>
        )}
      </header>

      {analysis ? (
        <>
          <RiskMatrix threats={analysis.threats} />
          <ComponentOverview components={analysis.architecture.components} />
          <ThreatTable threats={analysis.threats} />
          <ReportViewer markdown={analysis.report_markdown} />
        </>
      ) : (
        <div className="empty-state">No report generated yet.</div>
      )}
    </section>
  );
}
