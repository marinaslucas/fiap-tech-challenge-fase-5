import type { ArchitectureComponent } from "../types/architecture";

interface ComponentOverviewProps {
  components: ArchitectureComponent[];
  language?: "en" | "pt-BR";
}

export default function ComponentOverview({ components, language = "en" }: ComponentOverviewProps) {
  const labels =
    language === "pt-BR"
      ? {
          title: "Vis\u00e3o dos Componentes",
          type: "Tipo",
          zone: "Zona",
          exposure: "Exposi\u00e7\u00e3o",
          confidence: "Confian\u00e7a",
          unknown: "desconhecido",
          empty: "Nenhum componente detectado.",
        }
      : {
          title: "Component Overview",
          type: "Type",
          zone: "Zone",
          exposure: "Exposure",
          confidence: "Confidence",
          unknown: "unknown",
          empty: "No components detected.",
        };

  return (
    <section className="component-overview">
      <div className="panel-title">{labels.title}</div>
      <div className="component-grid">
        {components.map((component) => (
          <article className="component-card" key={component.id}>
            <div>
              <span className="component-id">{component.id}</span>
              <h2>{component.name}</h2>
            </div>
            <dl>
              <div>
                <dt>{labels.type}</dt>
                <dd>{component.type}</dd>
              </div>
              <div>
                <dt>{labels.zone}</dt>
                <dd>{component.zone ?? labels.unknown}</dd>
              </div>
              <div>
                <dt>{labels.exposure}</dt>
                <dd>{component.exposure ?? labels.unknown}</dd>
              </div>
              <div>
                <dt>{labels.confidence}</dt>
                <dd>{Math.round(component.confidence * 100)}%</dd>
              </div>
            </dl>
          </article>
        ))}
        {!components.length && <div className="empty-state">{labels.empty}</div>}
      </div>
    </section>
  );
}
