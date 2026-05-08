"use client";

import { Download, FileJson, FileText, Code } from "lucide-react";
import { useState } from "react";

interface ExportPanelProps {
  diagramSource: string;
  diagramFormat: string;
  explanation: string;
  disabled?: boolean;
}

export default function ExportPanel({
  diagramSource,
  diagramFormat,
  explanation,
  disabled = false,
}: ExportPanelProps) {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async (format: string) => {
    if (disabled || isExporting) return;

    setIsExporting(true);

    try {
      let content = "";
      let filename = "";
      let mimeType = "text/plain";

      switch (format) {
        case "mermaid":
          content = diagramSource;
          filename = "diagram.mmd";
          mimeType = "text/plain";
          break;
        case "json":
          content = JSON.stringify(
            {
              source: diagramSource,
              format: diagramFormat,
              explanation,
              exportedAt: new Date().toISOString(),
            },
            null,
            2,
          );
          filename = "diagram.json";
          mimeType = "application/json";
          break;
        case "enhanced-prompt":
          content = explanation;
          filename = "explanation.txt";
          mimeType = "text/plain";
          break;
        default:
          content = diagramSource;
          filename = "diagram.txt";
          mimeType = "text/plain";
      }

      // Create download
      const blob = new Blob([content], { type: mimeType });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Export failed:", error);
      alert("Export failed. Please try again.");
    } finally {
      setIsExporting(false);
    }
  };

  const exportOptions = [
    {
      id: "mermaid",
      label: "Mermaid",
      icon: Code,
      description: "Download as .mmd file",
    },
    {
      id: "json",
      label: "JSON",
      icon: FileJson,
      description: "Download as structured JSON",
    },
    {
      id: "enhanced-prompt",
      label: "Explanation",
      icon: FileText,
      description: "Download explanation text",
    },
  ];

  return (
    <div className="border-t border-gray-200 pt-4">
      <h3 className="text-sm font-medium text-gray-700 mb-3">Export Diagram</h3>
      <div className="grid grid-cols-3 gap-2">
        {exportOptions.map((option) => (
          <button
            key={option.id}
            type="button"
            onClick={() => handleExport(option.id)}
            disabled={disabled || isExporting}
            className="flex flex-col items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 p-3 text-sm transition hover:border-gray-400 hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <option.icon className="w-5 h-5 text-gray-600" />
            <span className="font-medium text-gray-700">{option.label}</span>
            <span className="text-xs text-gray-500 text-center">
              {option.description}
            </span>
          </button>
        ))}
      </div>
      {isExporting && (
        <p className="mt-2 text-xs text-gray-500">Exporting...</p>
      )}
    </div>
  );
}
