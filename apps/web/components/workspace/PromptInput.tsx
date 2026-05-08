"use client";

import { useState } from "react";

const DIAGRAM_TYPES = [
  { value: "auto", label: "Auto-detect" },
  { value: "design-system-architecture", label: "Design System Architecture" },
  { value: "component-hierarchy", label: "Component Hierarchy" },
  { value: "token-architecture", label: "Token Architecture" },
  { value: "design-to-code-workflow", label: "Design-to-Code Workflow" },
];

const EXAMPLE_PROMPTS = [
  "Show me the architecture of a design system with tokens, components, and a React app",
  "Create a component hierarchy for a button, input, form, and modal system",
  "Diagram the flow from Figma design tokens to Tailwind config to React components",
  "Show how primitive tokens feed into semantic tokens and then component styles",
];

interface PromptInputProps {
  onSubmit: (prompt: string, diagramType: string) => void;
  disabled: boolean;
}

export default function PromptInput({ onSubmit, disabled }: PromptInputProps) {
  const [prompt, setPrompt] = useState("");
  const [diagramType, setDiagramType] = useState("auto");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || disabled) return;
    onSubmit(prompt.trim(), diagramType);
    setPrompt("");
  };

  const useExample = (example: string) => {
    setPrompt(example);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <label htmlFor="diagram-type" className="text-sm font-medium text-gray-700">
          Diagram Type
        </label>
        <select
          id="diagram-type"
          value={diagramType}
          onChange={(e) => setDiagramType(e.target.value)}
          disabled={disabled}
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black disabled:opacity-50"
        >
          {DIAGRAM_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </div>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe your design system idea..."
        rows={4}
        disabled={disabled}
        className="w-full resize-none rounded-lg border border-gray-300 p-3 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black disabled:opacity-50"
      />

      <div className="flex items-center justify-between">
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_PROMPTS.map((example, i) => (
            <button
              key={i}
              type="button"
              onClick={() => useExample(example)}
              disabled={disabled}
              className="rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-xs text-gray-600 transition hover:border-gray-400 hover:bg-gray-100 disabled:opacity-50"
            >
              Example {i + 1}
            </button>
          ))}
        </div>
        <button
          type="submit"
          disabled={disabled || !prompt.trim()}
          className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {disabled ? "Processing..." : "Generate Diagram"}
        </button>
      </div>
    </form>
  );
}
