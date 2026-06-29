import type { Threat } from "../types/threat";

const severities = ["Critical", "High", "Medium", "Low"];

interface RiskMatrixProps {
  threats: Threat[];
}

export default function RiskMatrix({ threats }: RiskMatrixProps) {
  return (
    <div className="risk-grid" aria-label="Risk matrix">
      {severities.map((severity) => {
        const count = threats.filter((threat) => threat.severity === severity).length;
        return (
          <div className="risk-cell" key={severity}>
            <span>{severity}</span>
            <strong>{count}</strong>
          </div>
        );
      })}
    </div>
  );
}
