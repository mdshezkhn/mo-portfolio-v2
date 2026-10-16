"use client";

import { CERTIFICATIONS } from "@/lib/data";

/**
 * Certifications — ink-flood index.
 * A sticky heading and a count line on the left; a numbered list on the
 * right. On hover/focus a row floods with ink from left to right and the
 * text turns white. The whole section sits on a white band with hairline
 * top and bottom borders. (No links — the résumé lists no certificate
 * URLs, so nothing points anywhere.)
 */
export default function Certifications() {
  return (
    <section id="certifications" className="ct-band" aria-labelledby="cert-h">
      <style>{`
        .ct-band { background: var(--card); border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding-block: clamp(84px, 12vh, 140px); }
        .ct-grid { display: grid; grid-template-columns: minmax(0, .8fr) minmax(0, 1.2fr); gap: clamp(28px, 4vw, 72px); align-items: start; }
        @media (max-width: 860px) { .ct-grid { grid-template-columns: 1fr; } .ct-left { position: static !important; } }
        .ct-left { position: sticky; top: 110px; }
        .ct-count { font-family: var(--mono); font-size: 12px; letter-spacing: .18em; color: var(--faint); margin-top: 16px; }
        .ct-list { display: grid; }
        .ct-row {
          position: relative; isolation: isolate;
          display: grid; grid-template-columns: 58px 1fr auto; gap: 18px; align-items: baseline;
          padding: 26px 18px; border-bottom: 1px solid var(--line);
        }
        .ct-row:first-child { border-top: 1px solid var(--line); }
        .ct-row::before {
          content: ""; position: absolute; inset: 0; z-index: -1;
          background: var(--ink); transform: scaleX(0); transform-origin: 0 50%;
          transition: transform .55s var(--ease);
        }
        .ct-row:hover::before, .ct-row:focus-visible::before, .ct-row:focus-within::before { transform: scaleX(1); }
        .ct-row .no { font-family: var(--mono); font-size: 12px; color: var(--faint); transition: color .35s var(--ease) .08s; }
        .ct-row .t { font-size: clamp(16px, 1.7vw, 20px); font-weight: 640; letter-spacing: -0.025em; line-height: 1.3; transition: color .35s var(--ease) .08s; }
        .ct-row .i { font-size: 13px; color: var(--mute); transition: color .35s var(--ease) .08s; text-align: right; }
        .ct-row:hover .no, .ct-row:focus-visible .no,
        .ct-row:hover .t, .ct-row:focus-visible .t,
        .ct-row:hover .i, .ct-row:focus-visible .i { color: var(--paper); }
      `}</style>

      <div className="shell">
        <div className="ct-grid">
          <div className="ct-left rv">
            <span className="tag">04 — Certifications</span>
            <h2 id="cert-h" className="h2" style={{ marginTop: 14 }}>
              Always <span className="it">learning.</span>
            </h2>
            <p className="ct-count">{String(CERTIFICATIONS.length).padStart(2, "0")} CERTIFICATIONS · VERIFIED TRAINING</p>
          </div>

          <div className="ct-list rv" style={{ "--i": 1 } as React.CSSProperties}>
            {CERTIFICATIONS.map((c, i) => (
              <div key={c.title} className="ct-row" tabIndex={0} aria-label={`${c.title}, ${c.issuer}`}>
                <span className="no" aria-hidden="true">{String(i + 1).padStart(2, "0")}</span>
                <span className="t">{c.title}</span>
                <span className="i">{c.issuer}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
