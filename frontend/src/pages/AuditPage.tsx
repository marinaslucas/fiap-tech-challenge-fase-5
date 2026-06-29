import type { AnalysisResponse } from "../types/report";

interface AuditPageProps {
  analysis: AnalysisResponse | null;
}

export default function AuditPage({ analysis }: AuditPageProps) {
  if (!analysis) {
    return (
      <section className="page-grid">
        <header className="page-header">
          <div>
            <p className="eyebrow">Agent Trace</p>
            <h1>Audit</h1>
          </div>
        </header>
        <div className="empty-state">Run an analysis to inspect the agent trace.</div>
      </section>
    );
  }

  const { audit } = analysis;

  return (
    <section className="page-grid">
      <header className="page-header">
        <div>
          <p className="eyebrow">Agent Trace</p>
          <h1>Audit</h1>
        </div>
      </header>

      <div className="audit-grid">
        <Metric label="Detector inputs" value={audit.detector_input_count} />
        <Metric label="Normalized components" value={audit.normalized_component_count} />
        <Metric label="Threats" value={audit.threat_count} />
        <Metric label="Vulnerabilities" value={audit.vulnerability_count} />
        <Metric label="Countermeasures" value={audit.countermeasure_count} />
        <Metric label="Language" value={audit.report_language} />
      </div>

      <section className="audit-panel">
        <div className="panel-title">Execution Mode</div>
        <dl className="audit-facts">
          <div>
            <dt>Gemini configured</dt>
            <dd>{audit.gemini_configured ? "Yes" : "No"}</dd>
          </div>
          <div>
            <dt>Model</dt>
            <dd>{audit.gemini_model ?? "N/A"}</dd>
          </div>
          <div>
            <dt>LLM used</dt>
            <dd>{audit.llm_used ? "Yes" : "No"}</dd>
          </div>
          <div>
            <dt>Fallback used</dt>
            <dd>{audit.fallback_used ? "Yes" : "No"}</dd>
          </div>
          {audit.fallback_reason && (
            <div>
              <dt>Fallback reason</dt>
              <dd>{audit.fallback_reason}</dd>
            </div>
          )}
        </dl>
      </section>

      <section className="audit-panel">
        <div className="panel-title">Agent Log</div>
        <ol className="audit-list">
          {audit.agent_log.map((entry) => (
            <li key={entry}>{entry}</li>
          ))}
        </ol>
      </section>

      <section className="audit-panel">
        <div className="panel-title">Normalized Architecture JSON</div>
        <pre className="audit-code">{JSON.stringify(analysis.architecture, null, 2)}</pre>
      </section>

      {audit.stride_prompt && (
        <section className="audit-panel">
          <div className="panel-title">STRIDE Prompt</div>
          <pre className="audit-code">{audit.stride_prompt}</pre>
        </section>
      )}
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="audit-metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
