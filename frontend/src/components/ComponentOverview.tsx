import type { ArchitectureComponent } from "../types/architecture";

interface ComponentOverviewProps {
  components: ArchitectureComponent[];
}

export default function ComponentOverview({ components }: ComponentOverviewProps) {
  return (
    <section className="component-overview">
      <div className="panel-title">Component Overview</div>
      <div className="component-grid">
        {components.map((component) => (
          <article className="component-card" key={component.id}>
            <div>
              <span className="component-id">{component.id}</span>
              <h2>{component.name}</h2>
            </div>
            <dl>
              <div>
                <dt>Type</dt>
                <dd>{component.type}</dd>
              </div>
              <div>
                <dt>Zone</dt>
                <dd>{component.zone ?? "unknown"}</dd>
              </div>
              <div>
                <dt>Exposure</dt>
                <dd>{component.exposure ?? "unknown"}</dd>
              </div>
              <div>
                <dt>Confidence</dt>
                <dd>{Math.round(component.confidence * 100)}%</dd>
              </div>
            </dl>
          </article>
        ))}
        {!components.length && <div className="empty-state">No components detected.</div>}
      </div>
    </section>
  );
}
