import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Design System Diagram Assistant",
  description:
    "Transform design system ideas into structured diagrams using AI-powered prompt enhancement.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
