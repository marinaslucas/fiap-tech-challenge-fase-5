import type { ArchitectureComponent } from "../types/architecture";

interface ComponentSummaryProps {
  components: ArchitectureComponent[];
  language?: "en" | "pt-BR";
}

interface ComponentGroup {
  type: string;
  name: string;
  zone: string | null;
  exposure: string | null;
  count: number;
  confidenceTotal: number;
}

export default function ComponentSummary({ components, language = "en" }: ComponentSummaryProps) {
  const isPtBr = language === "pt-BR";
  const labels = isPtBr
    ? {
        title: "Inventário resumido",
        type: "Componente",
        count: "Quantidade",
        zone: "Zona",
        exposure: "Exposição",
        confidence: "Confiança média",
        unknown: "desconhecida",
      }
    : {
        title: "Component inventory summary",
        type: "Component",
        count: "Count",
        zone: "Zone",
        exposure: "Exposure",
        confidence: "Average confidence",
        unknown: "unknown",
      };

  const grouped = new Map<string, ComponentGroup>();
  for (const component of components) {
    const current = grouped.get(component.type);
    if (current) {
      current.count += 1;
      current.confidenceTotal += component.confidence;
      continue;
    }

    grouped.set(component.type, {
      type: component.type,
      name: component.name,
      zone: component.zone,
      exposure: component.exposure,
      count: 1,
      confidenceTotal: component.confidence,
    });
  }

  const groups = [...grouped.values()].sort(
    (left, right) => right.count - left.count || left.name.localeCompare(right.name),
  );

  return (
    <section className="component-summary print-only">
      <div className="panel-title">{labels.title}</div>
      <table>
        <thead>
          <tr>
            <th>{labels.type}</th>
            <th>{labels.count}</th>
            <th>{labels.zone}</th>
            <th>{labels.exposure}</th>
            <th>{labels.confidence}</th>
          </tr>
        </thead>
        <tbody>
          {groups.map((group) => (
            <tr key={group.type}>
              <td>
                <strong>{group.name}</strong>
                <small>{group.type}</small>
              </td>
              <td>{group.count}</td>
              <td>{group.zone ?? labels.unknown}</td>
              <td>{group.exposure ?? labels.unknown}</td>
              <td>{Math.round((group.confidenceTotal / group.count) * 100)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
