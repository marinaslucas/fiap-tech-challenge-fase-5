declare module "lucide-react" {
  import type { ComponentType, SVGProps } from "react";

  export interface LucideProps extends SVGProps<SVGSVGElement> {
    size?: string | number;
    absoluteStrokeWidth?: boolean;
  }

  export type LucideIcon = ComponentType<LucideProps>;

  export const FileDown: LucideIcon;
  export const FileSearch: LucideIcon;
  export const FileText: LucideIcon;
  export const History: LucideIcon;
  export const KeyRound: LucideIcon;
  export const Loader2: LucideIcon;
  export const Radar: LucideIcon;
  export const ShieldCheck: LucideIcon;
  export const UploadCloud: LucideIcon;
}
