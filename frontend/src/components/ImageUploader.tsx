import { UploadCloud } from "lucide-react";

interface ImageUploaderProps {
  disabled?: boolean;
  onFile: (file: File) => void;
}

export default function ImageUploader({ disabled, onFile }: ImageUploaderProps) {
  return (
    <label className={`upload-zone ${disabled ? "disabled" : ""}`}>
      <UploadCloud size={28} aria-hidden="true" />
      <span>{disabled ? "Processing diagram..." : "Upload architecture diagram"}</span>
      <input
        type="file"
        accept="image/*"
        disabled={disabled}
        onChange={(event) => {
          const file = event.currentTarget.files?.[0];
          if (file) {
            onFile(file);
          }
        }}
      />
    </label>
  );
}
