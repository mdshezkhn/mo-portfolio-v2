"use client";

import { useEffect, useRef, useState } from "react";
import { ABOUT_QUOTE, ASSET, ID_CARD, PROFILE, QUICK_FACTS } from "@/lib/data";
import { usePrefersReducedMotion } from "@/lib/hooks";

/**
 * About — the hanging lanyard ID card.
 * - Damped pendulum swing driven by pointer velocity (spring physics in rAF)
 * - Subtle idle sway when the pointer is away
 * - Card flips on hover; on touch it flips on tap; keyboard: Enter/Space
 * - Front: TEACHER ID band, portrait with halo, ID rows, barcode, holo sticker
 * - Back: "What I am" lines from the résumé + signature + say-hello line
 */
export default function About() {
  const [flipped, setFlipped] = useState(false);
  const reduced = usePrefersReducedMotion();
  const wrapRef = useRef<HTMLDivElement>(null);
  const cardRef = useRef<HTMLDivElement>(null);
  const state = useRef({ angle: 0, vel: 0, target: 0, lastX: 0, lastT: 0, idleAt: 0 });

  /* Pendulum physics */
  useEffect(() => {
    if (reduced) return;
    let raf = 0;
    const s = state.current;
    const tick = (t: number) => {
      const idle = t - s.idleAt > 1800;
      if (idle) s.target = Math.sin(t / 1400) * 2.2;          // idle sway
      const k = 0.016, damp = 0.055;                           // spring + damping
      s.vel += (s.target - s.angle) * k;
      s.vel *= 1 - damp;
      s.angle += s.vel;
      if (cardRef.current) {
        cardRef.current.style.transform = `rotateY(${flipped ? 180 : 0}deg) rotate(${s.angle.toFixed(3)}deg)`;
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);

    const onMove = (e: PointerEvent) => {
      const s2 = state.current;
      const now = performance.now();
      const dt = Math.max(8, now - s2.lastT);
      const vel = ((e.clientX - s2.lastX) / dt) * 16;         // px/ms → velocity
      s2.lastX = e.clientX; s2.lastT = now; s2.idleAt = now;
      s2.target = Math.max(-16, Math.min(16, s2.target + vel * 0.35));
    };
    window.addEventListener("pointermove", onMove);
    return () => { cancelAnimationFrame(raf); window.removeEventListener("pointermove", onMove); };
  }, [reduced, flipped]);

  return (
    <section id="about" className="section ab" aria-labelledby="about-h">
      <style>{`
        .ab-grid {
          display: grid;
          grid-template-columns: minmax(0,1fr) 320px minmax(0,1fr);
          gap: clamp(24px, 4vw, 56px);
          align-items: stretch;
        }
        @media (max-width: 980px) {
          .ab-grid { grid-template-columns: 1fr; }
          .ab-mid { order: -1; } /* card first on mobile */
        }
        .ab-h { margin-bottom: clamp(28px, 4vh, 44px); }
        .ab-hello { font-size: clamp(26px, 3vw, 38px); font-weight: 700; letter-spacing: -0.045em; line-height: 1.1; }
        .ab-sum { color: var(--ink-2); font-size: clamp(15.5px, 1.35vw, 17.5px); line-height: 1.75; margin: 18px 0 0; }
        .ab-extra { color: var(--mute); font-size: 15px; line-height: 1.7; margin: 14px 0 26px; }
        .ab-btns { display: flex; flex-wrap: wrap; gap: 12px; }

        /* lanyard */
        .ab-mid { display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding-top: 6px; }
        .ab-strap {
          width: 30px; height: 56px; overflow: hidden; position: relative;
          background: linear-gradient(180deg, #171717 0%, #262626 100%);
          box-shadow: inset 0 0 0 1px rgba(255,255,255,.06), 0 2px 6px rgba(13,13,13,.18);
          clip-path: polygon(14% 0, 86% 0, 100% 100%, 0 100%);
        }
        .ab-strap-txt {
          position: absolute; left: 50%; top: 0;
          writing-mode: vertical-rl; transform: translateX(-50%);
          font-family: var(--mono); font-size: 7px; letter-spacing: .32em; color: #9a9a9a;
          white-space: nowrap;
          animation: abStrap 9s linear infinite;
        }
        @keyframes abStrap { from { transform: translate(-50%, 0); } to { transform: translate(-50%, -50%); } }
        .ab-clip {
          width: 18px; height: 12px; margin-top: -1px; z-index: 2;
          background: linear-gradient(180deg, #d9d9d9, #9d9d9d);
          border-radius: 3px 3px 5px 5px;
          box-shadow: 0 1px 2px rgba(13,13,13,.3);
        }
        .ab-pivot { perspective: 1200px; width: 300px; display: flex; flex-direction: column; align-items: center; }
        .ab-card {
          position: relative; width: 300px; height: 404px; margin-top: 6px;
          transform-style: preserve-3d; transition: transform .9s var(--ease);
          will-change: transform;
        }
        .ab-card.ab-static { transform: rotateY(${flipped ? 180 : 0}deg); }
        .ab-face {
          position: absolute; inset: 0; border-radius: 18px; overflow: hidden;
          backface-visibility: hidden; -webkit-backface-visibility: hidden;
          background: linear-gradient(168deg, #fdfdfc 0%, #f1efeb 100%);
          box-shadow: inset 0 0 0 1px rgba(13,13,13,.12), 0 30px 60px -24px rgba(13,13,13,.35);
          padding: 18px 18px 14px;
          display: flex; flex-direction: column;
        }
        .ab-back { transform: rotateY(180deg); }
        .ab-band {
          margin: 0 -18px 14px; padding: 9px 18px;
          background: var(--ink); color: var(--paper);
          font-family: var(--mono); font-size: 10px; letter-spacing: .34em;
          display: flex; justify-content: space-between; align-items: center;
        }
        .ab-photo {
          width: 128px; height: 156px; margin: 0 auto; border-radius: 14px; overflow: hidden; position: relative;
          box-shadow: 0 0 0 3px #fff, 0 0 0 4px var(--line), 0 10px 26px -10px rgba(13,13,13,.35);
        }
        .ab-photo img { width: 100%; height: 100%; object-fit: cover; transition: transform 1s var(--ease); }
        .ab-card:hover .ab-photo img { transform: scale(1.07); }
        .ab-halo { position: absolute; inset: -34px; background: radial-gradient(closest-side, rgba(13,13,13,.14), transparent 72%); z-index: -1; }
        .ab-name { text-align: center; font-weight: 700; font-size: 17px; letter-spacing: -0.02em; margin-top: 14px; }
        .ab-role { text-align: center; color: var(--mute); font-size: 11.5px; line-height: 1.45; margin-top: 3px; }
        .ab-rows { margin-top: 12px; display: grid; gap: 6px; font-family: var(--mono); font-size: 10.5px; letter-spacing: .04em; }
        .ab-row { display: flex; justify-content: space-between; color: var(--ink-2); border-bottom: 1px dashed rgba(13,13,13,.14); padding-bottom: 5px; }
        .ab-row b { color: var(--mute); font-weight: 500; }
        .ab-foot { margin-top: auto; display: flex; align-items: flex-end; justify-content: space-between; padding-top: 12px; }
        .ab-barcode {
          width: 118px; height: 30px;
          background: repeating-linear-gradient(90deg, var(--ink) 0 2px, transparent 2px 4px, var(--ink) 4px 5px, transparent 5px 9px, var(--ink) 9px 12px, transparent 12px 14px);
        }
        .ab-holo {
          width: 30px; height: 30px; border-radius: 999px;
          background: conic-gradient(from 210deg, #d8d8d8, #f4f4f4, #c9c9c9, #efefef, #d8d8d8);
          box-shadow: inset 0 0 0 1px rgba(13,13,13,.18), 0 3px 8px -3px rgba(13,13,13,.4);
        }
        .ab-back h3 { font-family: var(--mono); font-size: 10px; letter-spacing: .3em; color: var(--mute); text-transform: uppercase; margin: 4px 0 14px; }
        .ab-back ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }
        .ab-back li { font-size: 13px; line-height: 1.5; color: var(--ink-2); padding-left: 16px; position: relative; }
        .ab-back li::before { content: "—"; position: absolute; left: 0; color: var(--faint); }
        .ab-sign { margin-top: auto; }
        .ab-sign .sig { font-family: var(--serif); font-style: italic; font-size: 26px; color: var(--ink); border-bottom: 1px solid var(--line); padding-bottom: 2px; display: inline-block; }
        .ab-sign .cap { font-family: var(--mono); font-size: 9.5px; letter-spacing: .18em; color: var(--faint); text-transform: uppercase; margin-top: 6px; }
        .ab-found { margin-top: 12px; font-size: 11.5px; color: var(--mute); }

        .ab-facts { display: grid; gap: 0; align-content: start; }
        .ab-fact { display: flex; gap: 16px; padding: 15px 2px; border-bottom: 1px solid var(--line); }
        .ab-fact .k { font-family: var(--mono); font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--mute); min-width: 108px; padding-top: 2px; }
        .ab-fact .v { font-size: 14.5px; color: var(--ink-2); line-height: 1.55; }
        .ab-quote { margin-top: 26px; padding: 22px 24px; }
        .ab-quote p { font-family: var(--serif); font-style: italic; font-size: 19px; line-height: 1.5; color: var(--ink-2); margin: 0; }
        .ab-quote .qm { font-family: var(--serif); font-size: 40px; line-height: 0; color: var(--soft); display: block; height: 18px; }
        @media (prefers-reduced-motion: reduce) { .ab-strap-txt { animation: none; } }
      `}</style>

      <div className="shell">
        <div className="ab-h rv">
          <span className="tag">01 — About</span>
          <h2 id="about-h" className="h2" style={{ marginTop: 14 }}>
            The teacher behind <span className="it">the card.</span>
          </h2>
        </div>

        <div className="ab-grid">
          {/* Left — verbatim résumé summary */}
          <div className="rv" style={{ "--i": 1 } as React.CSSProperties}>
            <p className="ab-hello">
              Hi, I&rsquo;m <span className="it" style={{ fontSize: "1.12em" }}>{PROFILE.firstName}.</span>
            </p>
            <p className="ab-sum">{PROFILE.resumeSummary}</p>
            <p className="ab-extra">{PROFILE.summaryExtraLine}</p>
            <div className="ab-btns">
              <a className="btn btn--primary" href={ASSET(PROFILE.resumePath)} download>Résumé</a>
              <a className="btn btn--ghost" href={PROFILE.linkedin} target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
            </div>
          </div>

          {/* Centre — hanging lanyard ID card */}
          <div className="ab-mid rv" style={{ "--i": 2 } as React.CSSProperties} ref={wrapRef}>
            <div className="ab-strap" aria-hidden="true">
              <span className="ab-strap-txt">{`${ID_CARD.strapText} · ${ID_CARD.strapText} · `}</span>
            </div>
            <div className="ab-clip" aria-hidden="true" />
            <div
              className="ab-pivot"
              onMouseEnter={() => setFlipped(true)}
              onMouseLeave={() => setFlipped(false)}
              onClick={() => setFlipped((f) => !f)}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setFlipped((f) => !f); } }}
              role="button"
              tabIndex={0}
              aria-pressed={flipped}
              aria-label={`ID card — ${PROFILE.name}. ${flipped ? "Showing back" : "Showing front"}. Activate to flip.`}
            >
              <div className={`ab-card ${reduced ? "ab-static" : ""}`} ref={cardRef} style={reduced ? undefined : { transform: "rotate(0deg)" }}>
                {/* FRONT */}
                <div className="ab-face" aria-hidden={flipped}>
                  <div className="ab-band"><span>{ID_CARD.band}</span><span>№</span></div>
                  <div className="ab-photo">
                    <span className="ab-halo" aria-hidden="true" />
                    <img src={ASSET("/portrait-bust.webp")} alt={`Portrait of ${PROFILE.name}`} />
                  </div>
                  <div className="ab-name">{PROFILE.name}</div>
                  <div className="ab-role">{PROFILE.role}</div>
                  <div className="ab-rows">
                    <div className="ab-row"><b>ID No.</b><span>{ID_CARD.idNo}</span></div>
                    <div className="ab-row"><b>Dept.</b><span>{ID_CARD.dept}</span></div>
                    <div className="ab-row"><b>Valid till</b><span>{ID_CARD.validTill}</span></div>
                  </div>
                  <div className="ab-foot">
                    <div className="ab-barcode" aria-hidden="true" />
                    <div className="ab-holo" aria-hidden="true" />
                  </div>
                </div>
                {/* BACK */}
                <div className="ab-face ab-back" aria-hidden={!flipped}>
                  <div className="ab-band"><span>{ID_CARD.band}</span><span>↺</span></div>
                  <h3>{ID_CARD.backTitle}</h3>
                  <ul>
                    {ID_CARD.backLines.map((l) => <li key={l}>{l}</li>)}
                  </ul>
                  <div className="ab-sign">
                    <span className="sig">{PROFILE.firstName}</span>
                    <div className="cap">Signature · Primary EAL</div>
                  </div>
                  <p className="ab-found">If found, say hello · {PROFILE.email}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right — quick facts + quote */}
          <div className="rv" style={{ "--i": 3 } as React.CSSProperties}>
            <div className="ab-facts">
              {QUICK_FACTS.map((f) => (
                <div className="ab-fact" key={f.k}>
                  <span className="k">{f.k}</span>
                  <span className="v">{f.v}</span>
                </div>
              ))}
            </div>
            <blockquote className="ab-quote card">
              <span className="qm" aria-hidden="true">&ldquo;</span>
              <p>{ABOUT_QUOTE}</p>
            </blockquote>
          </div>
        </div>
      </div>
    </section>
  );
}
