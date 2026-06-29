import type { Detection } from "../types/detection";

interface DetectionViewerProps {
  imageUrl: string | null;
  detections: Detection[];
  isBusy?: boolean;
}

export default function DetectionViewer({ imageUrl, detections, isBusy }: DetectionViewerProps) {
  return (
    <div className="viewer">
      <div className="viewer-frame">
        {imageUrl ? (
          <>
            <img src={imageUrl} alt="Uploaded architecture diagram" />
            {isBusy && <div className="viewer-overlay">Processing</div>}
          </>
        ) : (
          <div className="empty-state">No image selected.</div>
        )}
      </div>
      <div className="viewer-footer">
        <span>{detections.length} components</span>
        <span>{isBusy ? "Processing" : detections.some((item) => item.confidence < 0.8) ? "Review needed" : "Ready"}</span>
      </div>
    </div>
  );
}
