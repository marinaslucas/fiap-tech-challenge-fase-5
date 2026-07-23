import type { Countermeasure, SecurityReference, Threat, VulnerabilityFinding } from "../types/threat";

interface ReportFindingsProps {
  threats: Threat[];
  vulnerabilities: VulnerabilityFinding[];
  countermeasures: Countermeasure[];
  references: SecurityReference[];
  language?: "en" | "pt-BR";
}

export default function ReportFindings({
  threats,
  vulnerabilities,
  countermeasures,
  references,
  language = "en",
}: ReportFindingsProps) {
  const labels =
    language === "pt-BR"
      ? {
          title: "Achados, validações e contramedidas",
          evidence: "Evidência",
          confidence: "Confiança",
          vulnerabilities: "Riscos potenciais",
          countermeasures: "Contramedidas recomendadas",
          validation: "Perguntas de validação",
          references: "Referências",
        }
      : {
          title: "Findings, validation and countermeasures",
          evidence: "Evidence",
          confidence: "Confidence",
          vulnerabilities: "Potential risks",
          countermeasures: "Recommended countermeasures",
          validation: "Validation questions",
          references: "References",
        };

  return (
    <section className="report-findings print-only">
      <div className="section-heading">
        <p className="eyebrow">STRIDE</p>
        <h2>{labels.title}</h2>
      </div>
      <div className="finding-list">
        {threats.map((threat) => {
          const relatedVulnerabilities = vulnerabilities.filter((item) => item.threat_id === threat.id);
          const relatedCountermeasures = countermeasures.filter((item) => item.threat_id === threat.id);
          const relatedReferences = references.filter((item) => item.threat_id === threat.id);

          return (
            <article className="finding-card" key={threat.id}>
              <header>
                <div>
                  <span className={`severity-pill severity-${threat.severity.toLowerCase()}`}>
                    {threat.severity}
                  </span>
                  <span>{threat.id}</span>
                </div>
                <h3>{threat.stride_category}</h3>
                <p>{threat.description}</p>
              </header>
              <dl className="finding-evidence">
                <div>
                  <dt>{labels.evidence}</dt>
                  <dd>{threat.evidence}</dd>
                </div>
                <div>
                  <dt>{labels.confidence}</dt>
                  <dd>{threat.confidence}</dd>
                </div>
              </dl>

              {relatedVulnerabilities.length > 0 && (
                <section>
                  <h4>{labels.vulnerabilities}</h4>
                  <ul>
                    {relatedVulnerabilities.map((item) => (
                      <li key={`${item.threat_id}-${item.weakness}`}>{item.weakness}: {item.rationale}</li>
                    ))}
                  </ul>
                </section>
              )}

              {relatedCountermeasures.length > 0 && (
                <section>
                  <h4>{labels.countermeasures}</h4>
                  <ul>
                    {relatedCountermeasures.map((item) => (
                      <li key={`${item.threat_id}-${item.recommendation}`}>{item.recommendation}</li>
                    ))}
                  </ul>
                </section>
              )}

              {threat.needs_validation.length > 0 && (
                <section>
                  <h4>{labels.validation}</h4>
                  <ul>
                    {threat.needs_validation.map((question) => <li key={question}>{question}</li>)}
                  </ul>
                </section>
              )}

              {relatedReferences.length > 0 && (
                <section className="finding-references">
                  <h4>{labels.references}</h4>
                  <ul>
                    {relatedReferences.map((reference) => (
                      <li key={`${reference.source}-${reference.reference_id}`}>
                        <a href={reference.url}>{reference.source} {reference.reference_id}</a>: {reference.title}
                      </li>
                    ))}
                  </ul>
                </section>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
