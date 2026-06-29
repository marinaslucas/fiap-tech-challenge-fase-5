import type { Threat } from "../types/threat";

interface ThreatTableProps {
  threats: Threat[];
  language?: "en" | "pt-BR";
}

export default function ThreatTable({ threats, language = "en" }: ThreatTableProps) {
  const labels =
    language === "pt-BR"
      ? {
          title: "Amea\u00e7as",
          severity: "Severidade",
          confidence: "Confian\u00e7a",
          evidence: "Evid\u00eancia",
          empty: "Nenhuma amea\u00e7a gerada.",
        }
      : {
          title: "Threats",
          severity: "Severity",
          confidence: "Confidence",
          evidence: "Evidence",
          empty: "No threats generated.",
        };

  return (
    <div className="table-panel">
      <div className="panel-title">{labels.title}</div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>STRIDE</th>
            <th>{labels.severity}</th>
            <th>{labels.confidence}</th>
            <th>{labels.evidence}</th>
          </tr>
        </thead>
        <tbody>
          {threats.map((threat) => (
            <tr key={threat.id}>
              <td>{threat.id}</td>
              <td>{threat.stride_category}</td>
              <td>{threat.severity}</td>
              <td>{threat.confidence}</td>
              <td>{threat.evidence}</td>
            </tr>
          ))}
          {!threats.length && (
            <tr>
              <td colSpan={5}>{labels.empty}</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
