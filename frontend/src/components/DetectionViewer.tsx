import { useState } from "react";

import type { Detection } from "../types/detection";

interface DetectionViewerProps {
  imageUrl: string | null;
  detections: Detection[];
  isBusy?: boolean;
}

export default function DetectionViewer({ imageUrl, detections, isBusy }: DetectionViewerProps) {
  const [imageSize, setImageSize] = useState({
    naturalWidth: 0,
    naturalHeight: 0,
    renderedWidth: 0,
    renderedHeight: 0,
  });
  const scaleX = imageSize.naturalWidth ? imageSize.renderedWidth / imageSize.naturalWidth : 1;
  const scaleY = imageSize.naturalHeight ? imageSize.renderedHeight / imageSize.naturalHeight : 1;

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
                  renderedWidth: image.clientWidth,
                  renderedHeight: image.clientHeight,
                });
              }}
            />
            <div
              className="detection-layer"
              aria-hidden="true"
              style={{
                width: `${imageSize.renderedWidth}px`,
                height: `${imageSize.renderedHeight}px`,
              }}
            >
              {detections.map((detection, index) => {
                const left = detection.bbox.x1 * scaleX;
                const top = detection.bbox.y1 * scaleY;
                const width = (detection.bbox.x2 - detection.bbox.x1) * scaleX;
                const height = (detection.bbox.y2 - detection.bbox.y1) * scaleY;
                const colorIndex = index % 6;

                return (
                  <div
                    className={`detection-box detection-box-${colorIndex}`}
                    key={`${detection.component_type}-${index}`}
                    style={{
                      left: `${left}px`,
                      top: `${top}px`,
                      width: `${width}px`,
                      height: `${height}px`,
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
      <div className="viewer-footer">
        <span>{detections.length} components</span>
        <span>{isBusy ? "Processing" : detections.some((item) => item.confidence < 0.8) ? "Review needed" : "Ready"}</span>
      </div>
    </div>
  );
}
