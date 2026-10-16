import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { PROFILE } from "@/lib/data";

/* Self-hosted fonts — src/fonts, no external requests at runtime. */
const interTight = localFont({
  src: "../fonts/inter-tight-latin-wght-normal.woff2",
  variable: "--font-inter-tight",
  display: "swap",
});

const instrumentSerif = localFont({
  src: [
    { path: "../fonts/instrument-serif-latin-400-normal.woff2", weight: "400", style: "normal" },
    { path: "../fonts/instrument-serif-latin-400-italic.woff2", weight: "400", style: "italic" },
  ],
  variable: "--font-instrument-serif",
  display: "swap",
});

const jetbrainsMono = localFont({
  src: "../fonts/jetbrains-mono-latin-wght-normal.woff2",
  variable: "--font-jetbrains-mono",
  display: "swap",
});

const title = "Mohammed Shehzad Khan — International Primary EAL Educator";

export const metadata: Metadata = {
  metadataBase: new URL(PROFILE.portfolio),
  title,
  description: PROFILE.resumeSummary,
  keywords: ["EAL", "Primary Education", "TESOL", "International Teacher", "Zhengzhou"],
  authors: [{ name: PROFILE.name }],
  alternates: { canonical: PROFILE.portfolio },
  openGraph: {
    title,
    description: PROFILE.resumeSummary,
    url: PROFILE.portfolio,
    siteName: PROFILE.name,
    locale: "en_US",
    type: "website",
    images: [{ url: "/og.jpg", width: 1200, height: 630, alt: `${PROFILE.name} — ${PROFILE.role}` }],
  },
  twitter: { card: "summary_large_image", title, description: PROFILE.resumeSummary },
};

export const viewport: Viewport = {
  themeColor: "#f4f2ee",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${interTight.variable} ${instrumentSerif.variable} ${jetbrainsMono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
