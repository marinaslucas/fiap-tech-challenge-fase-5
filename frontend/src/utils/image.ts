const SVG_MIME_TYPE = "image/svg+xml";

export async function prepareImageForDetection(file: File): Promise<File> {
  if (!isSvg(file)) {
    return file;
  }

  return rasterizeSvg(file);
}

function isSvg(file: File): boolean {
  return file.type === SVG_MIME_TYPE || file.name.toLowerCase().endsWith(".svg");
}

async function rasterizeSvg(file: File): Promise<File> {
  const svgText = await file.text();
  const svgBlob = new Blob([svgText], { type: SVG_MIME_TYPE });
  const svgUrl = URL.createObjectURL(svgBlob);

  try {
    const image = await loadImage(svgUrl);
    const width = image.naturalWidth || getSvgSize(svgText, "width") || 1280;
    const height = image.naturalHeight || getSvgSize(svgText, "height") || 720;
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;

    const context = canvas.getContext("2d");
    if (!context) {
      throw new Error("Canvas is not available.");
    }

    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, width, height);
    context.drawImage(image, 0, 0, width, height);

    const pngBlob = await canvasToBlob(canvas);
    const baseName = file.name.replace(/\.svg$/i, "");
    return new File([pngBlob], `${baseName}.png`, { type: "image/png" });
  } finally {
    URL.revokeObjectURL(svgUrl);
  }
}

function loadImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error("Could not render SVG for detection."));
    image.src = url;
  });
}

function canvasToBlob(canvas: HTMLCanvasElement): Promise<Blob> {
  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (!blob) {
        reject(new Error("Could not convert SVG to PNG."));
        return;
      }
      resolve(blob);
    }, "image/png");
  });
}

function getSvgSize(svgText: string, attribute: "width" | "height"): number | null {
  const match = svgText.match(new RegExp(`${attribute}=["']?([0-9.]+)`));
  if (!match) {
    return null;
  }

  const value = Number.parseFloat(match[1]);
  return Number.isFinite(value) ? Math.round(value) : null;
}
