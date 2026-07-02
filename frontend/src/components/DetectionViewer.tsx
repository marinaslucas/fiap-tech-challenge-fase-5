import { useState } from "react";

import type { Detection } from "../types/detection";

interface DetectionViewerProps {
  imageUrl: string | null;
  detections: Detection[];
  isBusy?: boolean;
  showFooter?: boolean;
}

export default function DetectionViewer({
  imageUrl,
  detections,
  isBusy,
  showFooter = true,
}: DetectionViewerProps) {
  const [imageSize, setImageSize] = useState({
    naturalWidth: 0,
    naturalHeight: 0,
  });
  const canRenderDetections = imageSize.naturalWidth > 0 && imageSize.naturalHeight > 0;
  const toPercent = (value: number, total: number) =>
    `${Math.max(0, Math.min(100, (value / total) * 100))}%`;

  return (
    <div className="viewer">
      <div className="viewer-frame">
        {imageUrl ? (
          <>
            <img
              src={imageUrl}
              alt="Uploaded architecture diagram"
              onLoad={(event) => {
                const image = event.currentTarget;
                setImageSize({
                  naturalWidth: image.naturalWidth,
                  naturalHeight: image.naturalHeight,
                });
              }}
            />
            <div className="detection-layer" aria-hidden="true">
              {canRenderDetections && detections.map((detection, index) => {
                const colorIndex = index % 6;

                return (
                  <div
                    className={`detection-box detection-box-${colorIndex}`}
                    key={`${detection.component_type}-${index}`}
                    style={{
                      left: toPercent(detection.bbox.x1, imageSize.naturalWidth),
                      top: toPercent(detection.bbox.y1, imageSize.naturalHeight),
                      width: toPercent(detection.bbox.x2 - detection.bbox.x1, imageSize.naturalWidth),
                      height: toPercent(detection.bbox.y2 - detection.bbox.y1, imageSize.naturalHeight),
                    }}
                  >
                    <span>
                      {detection.component_type} {Math.round(detection.confidence * 100)}%
                    </span>
                  </div>
                );
              })}
            </div>
            {isBusy && <div className="viewer-overlay">Processing</div>}
          </>
        ) : (
          <div className="empty-state">No image selected.</div>
        )}
      </div>
      {showFooter && (
        <div className="viewer-footer">
          <span>{detections.length} components</span>
          <span>{isBusy ? "Processing" : detections.some((item) => item.confidence < 0.8) ? "Review needed" : "Ready"}</span>
        </div>
      )}
    </div>
  );
}
