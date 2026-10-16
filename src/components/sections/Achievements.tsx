"use client";

import { useEffect, useRef, useState } from "react";
import { ACHIEVEMENTS } from "@/lib/data";
import { usePrefersReducedMotion } from "@/lib/hooks";
import Counter from "../ui/Counter";

/**
 * Achievements — pinned horizontal gallery.
 * The section is sticky (100svh); its total height is the viewport plus
 * the horizontal travel. Scrolling slides the card track left; a thin
 * progress bar sits in the header. The card nearest the viewport centre
 * lifts 12px with a brighter glow. Numbers count up on first sight.
 * Reduced motion → the pin is removed and the track scrolls natively.
 * Only résumé-verifiable counts appear here (publication-policy safe).
 */
export default function Achievements() {
  const outerRef = useRef<HTMLElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);
  const barRef = useRef<HTMLSpanElement>(null);
  const cardRefs = useRef<(HTMLDivElement | null)[]>([]);
  const [travel, setTravel] = useState(0);
  const reduced = usePrefersReducedMotion();

  useEffect(() => {
    if (reduced) return;
    let raf = 0;

    const measure = () => {
      const track = trackRef.current;
      if (!track) return;
      setTravel(Math.max(0, track.scrollWidth - window.innerWidth + 2 * 0));
    };

    const update = () => {
      raf = 0;
      const outer = outerRef.current;
      const track = trackRef.current;
      if (!outer || !track) return;
      const r = outer.getBoundingClientRect();
      const vh = window.innerHeight;
      const span = Math.max(1, r.height - vh);
      const p = Math.min(1, Math.max(0, -r.top / span));
      track.style.transform = `translate3d(${-p * travel}px, 0, 0)`;
      if (barRef.current) barRef.current.style.transform = `scaleX(${p})`;

      /* nearest card to viewport centre lifts */
      const cx = window.innerWidth / 2;
      let best = -1, bestD = Infinity;
      cardRefs.current.forEach((c, i) => {
        if (!c) return;
        const b = c.getBoundingClientRect();
        const d = Math.abs(b.left + b.width / 2 - cx);
        if (d < bestD) { bestD = d; best = i; }
      });
      cardRefs.current.forEach((c, i) => { c?.classList.toggle("ac-card--near", i === best); });
    };

    const onScroll = () => { if (!raf) raf = requestAnimationFrame(update); };
    measure();
    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", () => { measure(); update(); });
    return () => { window.removeEventListener("scroll", onScroll); if (raf) cancelAnimationFrame(raf); };
  }, [travel, reduced]);

  const staticMode = reduced;

  return (
    <section
      id="achievements"
      ref={outerRef}
      className="ac"
      aria-labelledby="ac-h"
      style={{ height: staticMode ? "auto" : `calc(100svh + ${travel}px)` }}
    >
      <style>{`
        .ac { position: relative; background: var(--paper); }
        .ac-pin { position: sticky; top: 0; height: 100svh; display: flex; flex-direction: column; justify-content: center; overflow: hidden; }
        .ac-head { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin-bottom: clamp(22px, 4vh, 44px); }
        .ac-prog { width: clamp(120px, 22vw, 300px); height: 2px; background: var(--line); border-radius: 2px; overflow: hidden; }
        .ac-prog i { display: block; height: 100%; background: var(--ink); transform: scaleX(0); transform-origin: 0 50%; }
        .ac-track { display: flex; gap: clamp(16px, 2vw, 28px); padding-inline: var(--gutter); width: max-content; will-change: transform; }
        .ac-card {
          width: clamp(340px, 40vw, 540px); height: clamp(260px, 36vh, 310px);
          background: var(--card); border-radius: 28px;
          box-shadow: inset 0 0 0 1px rgba(13,13,13,.08), 0 10px 30px -18px rgba(13,13,13,.18);
          padding: clamp(20px, 2.4vw, 30px);
          display: flex; flex-direction: column;
          transition: transform .5s var(--ease), box-shadow .5s var(--ease);
        }
        .ac-card--near { transform: translateY(-12px); box-shadow: inset 0 0 0 1px rgba(13,13,13,.1), 0 30px 56px -24px rgba(13,13,13,.3); }
        .ac-top { display: flex; align-items: flex-start; justify-content: space-between; }
        .ac-tile {
          width: 72px; height: 72px; border-radius: 20px;
          display: grid; place-items: center;
          font-family: var(--mono); font-weight: 600; font-size: 19px; letter-spacing: .02em;
          background: var(--card); color: var(--ink-2);
          box-shadow: inset 0 0 0 1.5px rgba(13,13,13,.16), 0 14px 26px -16px rgba(13,13,13,.28);
        }
        .ac-idx { font-family: var(--mono); font-size: 11px; letter-spacing: .18em; color: var(--faint); }
        .ac-label { font-size: clamp(17px, 1.7vw, 21px); font-weight: 680; letter-spacing: -0.035em; line-height: 1.15; margin-top: auto; }
        .ac-caption { font-size: 13px; color: var(--mute); margin-top: 7px; line-height: 1.5; }
        .ac-detail { font-size: 11.5px; color: var(--faint); margin-top: 4px; font-family: var(--mono); letter-spacing: .04em; }
        .ac-bottom { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; }
        .ac-num { font-weight: 800; font-size: clamp(52px, 6vw, 84px); letter-spacing: -0.05em; line-height: .9; font-variant-numeric: tabular-nums; }
        .ac-numunit { font-family: var(--mono); font-size: 10.5px; letter-spacing: .2em; text-transform: uppercase; color: var(--faint); margin-top: 8px; }
        .ac-end {
          width: clamp(280px, 32vw, 420px); height: clamp(260px, 36vh, 310px);
          display: grid; place-items: center; border-radius: 28px;
          box-shadow: inset 0 0 0 1.5px dashed rgba(13,13,13,.22);
          font-size: clamp(22px, 2.4vw, 30px); font-weight: 680; letter-spacing: -0.04em;
        }
        .ac-scrollhint { font-family: var(--mono); font-size: 10.5px; letter-spacing: .2em; text-transform: uppercase; color: var(--faint); text-align: right; }
        @media (max-width: 760px) {
          .ac-track { padding-inline: var(--gutter); }
          .ac-card { width: 78vw; }
        }
        /* reduced motion: native horizontal scroller, no pin */
        .ac--static .ac-pin { position: static; height: auto; padding-block: 40px; }
        .ac--static .ac-track { transform: none !important; overflow-x: auto; width: auto; }
      `}</style>

      <div className={`ac-pin ${staticMode ? "ac--static" : ""}`} style={staticMode ? { height: "auto", paddingTop: 40, paddingBottom: 40 } : undefined}>
        <div className="shell ac-head">
          <div>
            <span className="tag">05 — Achievements</span>
            <h2 id="ac-h" className="h2" style={{ marginTop: 12 }}>
              Numbers that <span className="it">count.</span>
            </h2>
          </div>
          <div style={{ display: "grid", gap: 10, justifyItems: "end" }}>
            {!staticMode && (
              <span className="ac-scrollhint" aria-hidden="true">Scroll ↓ to browse →</span>
            )}
            <span className="ac-prog" aria-hidden="true"><i ref={barRef as React.RefObject<HTMLElement>} /></span>
          </div>
        </div>

        <div className={`ac-track ${staticMode ? "ac--static" : ""}`} ref={trackRef} style={staticMode ? { overflowX: "auto" } : undefined}>
          {ACHIEVEMENTS.map((a, i) => (
            <div
              key={a.label}
              className="ac-card"
              ref={(el) => { cardRefs.current[i] = el; }}
            >
              <div className="ac-top">
                <span className="ac-tile" aria-hidden="true">{a.tile}</span>
                <span className="ac-idx">{String(i + 1).padStart(2, "0")} / {String(ACHIEVEMENTS.length).padStart(2, "0")}</span>
              </div>
              <div className="ac-bottom" style={{ marginTop: "auto" }}>
                <div>
                  <div className="ac-label">{a.label}</div>
                  <div className="ac-caption">{a.caption}</div>
                  <div className="ac-detail">{a.detail}</div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div className="ac-num"><Counter to={a.number} suffix={a.suffix} /></div>
                  <div className="ac-numunit">{a.numberLabel}</div>
                </div>
              </div>
            </div>
          ))}
          <div className="ac-end"><span>and counting <span className="it">→</span></span></div>
        </div>
      </div>
    </section>
  );
}
