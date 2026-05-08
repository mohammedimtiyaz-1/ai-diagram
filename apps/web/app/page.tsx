"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

const EXAMPLES = [
  "Design system with tokens, components, Storybook, and a Next.js app",
  "Component hierarchy for a React UI kit: button, input, card, modal",
  "Flow from Figma tokens to Tailwind config to React components",
  "Token architecture: primitive, semantic, and component-level tokens",
];

export default function LandingPage() {
  const router = useRouter();

  const tryExample = (text: string) => {
    router.push(`/workspace`);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4 text-center">
      <h1 className="mb-4 text-4xl font-bold tracking-tight sm:text-6xl">
        AI Design System Diagram Assistant
      </h1>
      <p className="mb-8 max-w-2xl text-lg text-gray-600">
        Describe your design system ideas in plain text. We enhance your prompts
        with AI, generate structured Mermaid diagrams, and let you refine them
        conversationally.
      </p>

      <Link
        href="/workspace"
        className="mb-10 rounded-lg bg-black px-6 py-3 font-medium text-white transition hover:bg-gray-800"
      >
        Start Creating Diagrams
      </Link>

      <div className="w-full max-w-2xl">
        <p className="mb-3 text-sm font-medium uppercase tracking-wider text-gray-400">
          Try an example
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          {EXAMPLES.map((example, i) => (
            <button
              key={i}
              onClick={() => tryExample(example)}
              className="rounded-full border border-gray-200 bg-gray-50 px-4 py-2 text-sm text-gray-700 transition hover:border-gray-400 hover:bg-gray-100"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      <footer className="mt-16 text-xs text-gray-400">
        Built with Next.js + FastAPI + OpenAI + Mermaid
      </footer>
    </main>
  );
}
