"use client";

import { useState } from "react";

interface FollowUpInputProps {
  onSubmit: (prompt: string) => void;
  disabled: boolean;
}

export default function FollowUpInput({ onSubmit, disabled }: FollowUpInputProps) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || disabled) return;
    onSubmit(prompt.trim());
    setPrompt("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Ask to refine the diagram..."
        disabled={disabled}
        className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={disabled || !prompt.trim()}
        className="rounded-lg bg-gray-800 px-4 py-2 text-sm font-medium text-white transition hover:bg-black disabled:cursor-not-allowed disabled:opacity-40"
      >
        {disabled ? "..." : "Refine"}
      </button>
    </form>
  );
}
