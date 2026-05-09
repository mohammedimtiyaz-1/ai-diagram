"use client";

import { useState } from "react";
import { useWorkspaceStore } from "@/stores/workspace";

const CODEBASE_DIAGRAM_TYPES = [
  { value: "architecture", label: "System Architecture" },
  { value: "folder-structure", label: "Folder & Module Map" },
  { value: "component-dependencies", label: "Component Dependency Graph" },
  { value: "api-flow", label: "API & Data Flow" },
];

const NODE_THEMES = [
  { value: "default", label: "Default" },
  { value: "technical", label: "Technical" },
  { value: "soft", label: "Soft" },
  { value: "colorful", label: "Colorful" },
  { value: "dark", label: "Dark" },
];

interface CodebaseInputProps {
  onSubmit: (repoUrl: string, diagramType: string, nodeTheme: string) => void;
  disabled: boolean;
}

export default function CodebaseInput({ onSubmit, disabled }: CodebaseInputProps) {
  const repoUrl = useWorkspaceStore((s) => s.repoUrl);
  const nodeTheme = useWorkspaceStore((s) => s.selectedNodeTheme);
  const setRepoUrl = useWorkspaceStore((s) => s.setRepoUrl);
  const setNodeTheme = useWorkspaceStore((s) => s.setSelectedNodeTheme);

  const [diagramType, setDiagramType] = useState("architecture");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!repoUrl.trim() || disabled) return;
    
    // Simple validation
    if (!repoUrl.includes("github.com")) {
      alert("Please enter a valid GitHub repository URL");
      return;
    }
    
    onSubmit(repoUrl.trim(), diagramType, nodeTheme);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="codebase-diagram-type" className="text-sm font-medium text-gray-700">
            Diagram Type
          </label>
          <select
            id="codebase-diagram-type"
            value={diagramType}
            onChange={(e) => setDiagramType(e.target.value)}
            disabled={disabled}
            className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black disabled:opacity-50"
          >
            {CODEBASE_DIAGRAM_TYPES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="node-theme" className="text-sm font-medium text-gray-700">
            Visual Theme
          </label>
          <select
            id="node-theme"
            value={nodeTheme}
            onChange={(e) => setNodeTheme(e.target.value)}
            disabled={disabled}
            className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black disabled:opacity-50"
          >
            {NODE_THEMES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="repo-url" className="text-sm font-medium text-gray-700">
          GitHub Repository URL
        </label>
        <div className="flex flex-col sm:flex-row gap-2">
          <input
            id="repo-url"
            type="url"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/owner/repo"
            disabled={disabled}
            className="flex-1 rounded-lg border border-gray-300 p-2.5 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black disabled:opacity-50 min-w-0"
          />
          <button
            type="submit"
            disabled={disabled || !repoUrl.trim()}
            className="rounded-lg bg-black px-4 sm:px-6 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40 shrink-0"
          >
            {disabled ? "..." : "Analyze"}
          </button>
        </div>
        <p className="text-[10px] text-gray-500 italic">
          Supports public repositories only. We'll analyze the file tree and key files to map the architecture.
        </p>
      </div>
    </form>
  );
}
