import type { Detection } from "../types/detection";

interface ComponentTableProps {
  detections: Detection[];
  isBusy?: boolean;
}

export default function ComponentTable({ detections, isBusy }: ComponentTableProps) {
  return (
    <div className="table-panel">
      <div className="panel-title">Components</div>
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Confidence</th>
            <th>Box</th>
          </tr>
        </thead>
        <tbody>
          {detections.map((detection, index) => (
            <tr key={`${detection.component_type}-${index}`}>
              <td>{detection.component_type}</td>
              <td>{Math.round(detection.confidence * 100)}%</td>
              <td>
                {Math.round(detection.bbox.x1)}, {Math.round(detection.bbox.y1)}
              </td>
            </tr>
          ))}
          {isBusy && !detections.length && (
            <tr>
              <td colSpan={3}>Detector is processing the uploaded image.</td>
            </tr>
          )}
          {!isBusy && !detections.length && (
            <tr>
              <td colSpan={3}>No detections loaded.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
