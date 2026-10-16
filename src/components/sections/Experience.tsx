"use client";

import { useEffect, useRef, useState } from "react";
import { EXPERIENCE } from "@/lib/data";
import { usePrefersReducedMotion } from "@/lib/hooks";

/**
 * Experience — education and employment as one path.
 * A vertical timeline whose spine draws with scroll progress; each stop
 * lights up as the spine reaches it. Ends with a dashed "next" card.
 */
export default function Experience() {
  const ref = useRef<HTMLDivElement>(null);
  const [p, setP] = useState(0);
  const [lit, setLit] = useState<boolean[]>(() => EXPERIENCE.map(() => false));
  const reduced = usePrefersReducedMotion();

  useEffect(() => {
    if (reduced) { setP(1); setLit(EXPERIENCE.map(() => true)); return; }
    let raf = 0;
    const update = () => {
      const el = ref.current;
      if (!el) return;
      const r = el.getBoundingClientRect();
      const vh = window.innerHeight;
      const total = r.height - vh * 0.2;
      const prog = Math.min(1, Math.max(0, (vh * 0.78 - r.top) / Math.max(1, total)));
      setP(prog);
      const stopEls = el.querySelectorAll<HTMLElement>(".xp-stop");
      setLit((prev) => {
        const next = prev.slice();
        stopEls.forEach((s, i) => {
          if (s.getBoundingClientRect().top < vh * 0.72) next[i] = true;
        });
        return next.some((v, i) => v !== prev[i]) ? next : prev;
      });
      raf = 0;
    };
    const onScroll = () => { if (!raf) raf = requestAnimationFrame(update); };
    update();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => { window.removeEventListener("scroll", onScroll); window.removeEventListener("resize", onScroll); if (raf) cancelAnimationFrame(raf); };
  }, [reduced]);

  return (
    <section id="experience" className="section xp" aria-labelledby="xp-h">
      <style>{`
        .xp-head { margin-bottom: 40px; }
        .xp-wrap { position: relative; padding-left: clamp(30px, 4.5vw, 56px); }
        .xp-spine {
          position: absolute; left: 8px; top: 6px; bottom: 60px; width: 2px;
          background: var(--line); border-radius: 2px;
        }
        .xp-spine i { position: absolute; inset: 0; background: var(--ink); border-radius: 2px; transform-origin: 0 0; transform: scaleY(${p}); transition: transform .18s linear; }
        .xp-stop { position: relative; padding: 0 0 clamp(30px, 4.5vh, 46px) 0; display: grid; gap: 5px; }
        .xp-dot {
          position: absolute; left: calc(clamp(30px, 4.5vw, 56px) * -1); top: 7px;
          width: 18px; height: 18px; border-radius: 999px;
          background: var(--paper); box-shadow: inset 0 0 0 1.5px var(--faint);
          display: grid; place-items: center;
          transition: box-shadow .5s var(--ease), transform .5s var(--ease);
        }
        .xp-stop--lit .xp-dot { box-shadow: inset 0 0 0 6px var(--ink); transform: scale(1.05); }
        .xp-stop .yr { font-family: var(--mono); font-size: 11.5px; letter-spacing: .16em; color: var(--mute); text-transform: uppercase; transition: color .5s var(--ease); }
        .xp-stop--lit .yr { color: var(--ink); }
        .xp-stop .tt { font-size: clamp(18px, 2vw, 24px); font-weight: 680; letter-spacing: -0.035em; line-height: 1.15; color: var(--faint); transition: color .5s var(--ease); }
        .xp-stop--lit .tt { color: var(--ink); }
        .xp-stop .pl { font-size: 14px; color: var(--mute); transition: color .5s var(--ease); }
        .xp-stop--lit .pl { color: var(--ink-2); }
        .xp-stop .dt { font-size: 13.5px; line-height: 1.65; color: var(--faint); max-width: 62ch; transition: color .5s var(--ease); }
        .xp-stop--lit .dt { color: var(--mute); }
        .xp-kind { display: inline-block; font-family: var(--mono); font-size: 9px; letter-spacing: .2em; text-transform: uppercase; padding: 4px 9px; border-radius: 999px; color: var(--mute); box-shadow: inset 0 0 0 1px var(--line); margin-top: 4px; }
        .xp-next {
          border: 1.5px dashed rgba(13,13,13,.25); border-radius: 22px;
          padding: 26px 28px; display: flex; align-items: baseline; justify-content: space-between; gap: 18px; flex-wrap: wrap;
        }
        .xp-next .t { font-size: clamp(18px, 2vw, 23px); font-weight: 680; letter-spacing: -0.035em; }
        .xp-next .t .it { font-size: 1.06em; }
      `}</style>

      <div className="shell">
        <div className="xp-head rv">
          <span className="tag">05 — Experience</span>
          <h2 id="xp-h" className="h2" style={{ marginTop: 14, maxWidth: "22ch" }}>
            One path, two decades of <span className="it">learning.</span>
          </h2>
        </div>

        <div className="xp-wrap" ref={ref}>
          <div className="xp-spine" aria-hidden="true"><i /></div>

          {EXPERIENCE.map((s, i) => (
            <div key={`${s.years}-${s.title}`} className={`xp-stop ${lit[i] ? "xp-stop--lit" : ""}`}>
              <span className="xp-dot" aria-hidden="true" />
              <span className="yr">{s.years}</span>
              <h3 className="tt">{s.title}</h3>
              <span className="pl">{s.place}</span>
              <p className="dt">{s.detail}</p>
              <span className="xp-kind">{s.kind === "education" ? "Education" : "Employment"}</span>
            </div>
          ))}

          <div className="xp-next rv">
            <span className="t">Next — <span className="it">your school?</span></span>
            <a className="btn btn--primary" href="#contact" onClick={(e) => { e.preventDefault(); document.getElementById("contact")?.scrollIntoView({ behavior: "smooth" }); }}>
              Let&rsquo;s talk
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
