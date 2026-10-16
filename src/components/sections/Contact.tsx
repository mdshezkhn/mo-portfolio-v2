"use client";

import { useState } from "react";
import { PROFILE } from "@/lib/data";
import { usePrefersReducedMotion } from "@/lib/hooks";
import { useScroll } from "@/lib/scroll";

/**
 * Contact + footer.
 * - Huge two-line heading; each letter hops as the cursor passes over it
 * - Email as a large underlined link + Copy chip ("Copied ✓", aria-live)
 * - Phone (tel:), LinkedIn and portfolio links — all from the résumé
 * - Circular "say hello" badge spinning slowly
 * - Footer: © year + name, Back to top, Built with Next.js
 */
export default function Contact() {
  const [copied, setCopied] = useState(false);
  const reduced = usePrefersReducedMotion();
  const { scrollToTarget } = useScroll();
  const year = new Date().getFullYear();

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(PROFILE.email);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = PROFILE.email; document.body.appendChild(ta); ta.select();
      document.execCommand("copy"); ta.remove();
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const line1 = "Let's build";
  const line2 = "something together.";

  return (
    <section id="contact" className="section ct" aria-labelledby="ct-h">
      <style>{`
        .ct-inner { position: relative; }
        .ct-title { font-size: clamp(44px, 8.4vw, 118px); font-weight: 800; letter-spacing: -0.05em; line-height: 0.98; margin: 22px 0 0; }
        .ct-l { display: inline-block; }
        .ct-l:hover { animation: ctHop .42s var(--ease); }
        @keyframes ctHop { 0% { transform: translateY(0); } 35% { transform: translateY(-0.24em); } 100% { transform: translateY(0); } }
        .ct-mail { margin-top: clamp(30px, 5vh, 54px); display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
        .ct-mail a { font-size: clamp(21px, 3.4vw, 42px); font-weight: 640; letter-spacing: -0.03em; }
        .ct-copy { min-width: 96px; justify-content: center; }
        .ct-links { margin-top: clamp(26px, 4vh, 40px); display: flex; flex-wrap: wrap; gap: 12px; }
        .ct-badge { position: absolute; right: clamp(0px, 2vw, 40px); top: -34px; width: 118px; height: 118px; pointer-events: none; }
        @media (max-width: 760px) { .ct-badge { display: none; } }
        .ct-badge svg { width: 100%; height: 100%; animation: ctSpin 16s linear infinite; }
        @keyframes ctSpin { to { transform: rotate(360deg); } }
        .ct-foot {
          margin-top: clamp(70px, 10vh, 120px); padding-top: 26px;
          border-top: 1px solid var(--line);
          display: flex; flex-wrap: wrap; gap: 14px; align-items: center; justify-content: space-between;
          font-family: var(--mono); font-size: 11.5px; letter-spacing: .08em; color: var(--mute);
        }
        .ct-foot a { text-decoration: underline; text-decoration-color: rgba(13,13,13,.25); text-underline-offset: 4px; }
        .ct-foot a:hover { text-decoration-color: var(--ink); }
        @media (prefers-reduced-motion: reduce) { .ct-l:hover { animation: none; } .ct-badge svg { animation: none; } }
      `}</style>

      <div className="shell ct-inner">
        <span className="tag rv">06 — Contact</span>

        <h2 id="ct-h" className="ct-title rv" style={{ "--i": 1 } as React.CSSProperties}>
          <Hop text={line1} />{" "}<span className="it"><Hop text={line2} /></span>
        </h2>

        <div className="ct-mail rv" style={{ "--i": 2 } as React.CSSProperties}>
          <a className="u-link" href={`mailto:${PROFILE.email}`}>{PROFILE.email}</a>
          <button className={`btn ${copied ? "btn--primary" : "btn--ghost"} ct-copy`} onClick={copy} aria-label="Copy email address">
            {copied ? "Copied ✓" : "Copy"}
          </button>
          <span aria-live="polite" className="sr-only">{copied ? "Email copied to clipboard" : ""}</span>
        </div>

        <div className="ct-links rv" style={{ "--i": 3 } as React.CSSProperties}>
          <a className="btn btn--ghost" href={`tel:${PROFILE.phoneHref}`}>{PROFILE.phone}</a>
          <a className="btn btn--ghost" href={PROFILE.linkedin} target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
          <a className="btn btn--ghost" href={PROFILE.portfolio} target="_blank" rel="noopener noreferrer">Portfolio ↗</a>
        </div>

        {/* spinning say-hello badge */}
        <div className="ct-badge" aria-hidden="true">
          <svg viewBox="0 0 120 120">
            <defs><path id="ct-circle" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0" /></defs>
            <text fontSize="11.5" letterSpacing="3.4" fill="#77756f" fontFamily="var(--mono)">
              <textPath href="#ct-circle">SAY HELLO · SAY HELLO · SAY HELLO ·</textPath>
            </text>
            <circle cx="60" cy="60" r="4" fill="#0d0d0d" />
          </svg>
        </div>

        <footer className="ct-foot rv" style={{ "--i": 4 } as React.CSSProperties}>
          <span>© {year} {PROFILE.name}</span>
          <div style={{ display: "flex", gap: 18, flexWrap: "wrap" }}>
            <a href="#hero" onClick={(e) => { e.preventDefault(); scrollToTarget("#hero"); }}>Back to top ↑</a>
            <span aria-hidden="true">·</span>
            <span>Built with Next.js</span>
          </div>
        </footer>
      </div>
    </section>
  );
}

/** Splits text into individually hoverable letters (skips spaces). */
function Hop({ text }: { text: string }) {
  return (
    <>
      {text.split("").map((ch, i) =>
        ch === " " ? <span key={i}>&nbsp;</span> : <span className="ct-l" key={i}>{ch}</span>
      )}
    </>
  );
}
