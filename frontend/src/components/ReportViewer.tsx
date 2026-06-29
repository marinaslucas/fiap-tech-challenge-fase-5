interface ReportViewerProps {
  markdown: string;
}

export default function ReportViewer({ markdown }: ReportViewerProps) {
  return (
    <div className="report-viewer">
      <div className="panel-title">Markdown Report</div>
      <pre>{markdown}</pre>
    </div>
  );
}
