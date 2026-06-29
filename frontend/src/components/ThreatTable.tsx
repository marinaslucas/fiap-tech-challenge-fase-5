import type { Threat } from "../types/threat";

interface ThreatTableProps {
  threats: Threat[];
}

export default function ThreatTable({ threats }: ThreatTableProps) {
  return (
    <div className="table-panel">
      <div className="panel-title">Threats</div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>STRIDE</th>
            <th>Severity</th>
            <th>Confidence</th>
            <th>Evidence</th>
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
              <td colSpan={5}>No threats generated.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
