"use client";

import { useState } from "react";
import VoiceInput from "./VoiceInput";

interface FollowUpInputProps {
  onSubmit: (prompt: string) => void;
  disabled: boolean;
}

const MIN_PROMPT_LENGTH = 3;

export default function FollowUpInput({ onSubmit, disabled }: FollowUpInputProps) {
  const [prompt, setPrompt] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = prompt.trim();
    
    if (!trimmed) return;
    if (disabled) return;
    if (trimmed.length < MIN_PROMPT_LENGTH) {
      setError(`Please enter at least ${MIN_PROMPT_LENGTH} characters.`);
      return;
    }
    
    setError("");
    onSubmit(trimmed);
    setPrompt("");
  };

  const handleTranscript = (transcript: string) => {
    setPrompt((prev) => {
      const newText = prev ? `${prev} ${transcript}` : transcript;
      return newText;
    });
    setError("");
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPrompt(e.target.value);
    setError("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2">
      <div className="flex flex-col sm:flex-row gap-2">
        <div className="relative flex-1 min-w-0">
          <input
            type="text"
            value={prompt}
            onChange={handleChange}
            placeholder="Ask to refine the diagram..."
            disabled={disabled}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 pr-10 text-sm focus:border-black focus:outline-none focus:ring-1 focus:ring-black disabled:opacity-50"
          />
          <div className="absolute right-1 top-1/2 -translate-y-1/2 scale-75">
            <VoiceInput onTranscript={handleTranscript} disabled={disabled} />
          </div>
        </div>
        <button
          type="submit"
          disabled={disabled || !prompt.trim()}
          className="rounded-lg bg-gray-800 px-4 py-2 text-sm font-medium text-white transition hover:bg-black disabled:cursor-not-allowed disabled:opacity-40 shrink-0"
        >
          {disabled ? "..." : "Refine"}
        </button>
      </div>
      {error && (
        <div className="text-xs text-red-600">{error}</div>
      )}
    </form>
  );
}
