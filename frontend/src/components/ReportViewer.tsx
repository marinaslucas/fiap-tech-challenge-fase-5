import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ReportViewerProps {
  markdown: string;
}

export default function ReportViewer({ markdown }: ReportViewerProps) {
  return (
    <div className="report-viewer screen-report-only">
      <div className="panel-title">Report</div>
      <div className="markdown-body">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
      </div>
    </div>
  );
}
