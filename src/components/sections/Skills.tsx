"use client";

import { useMemo, useState } from "react";
import { ALL_SKILLS, PROJECTS, SKILL_GROUPS, type Skill, type SkillFamily } from "@/lib/data";
import { useInView, usePrefersReducedMotion } from "@/lib/hooks";
import TechLogo, { isBrand } from "../ui/TechLogo";

/**
 * Skills — "the periodic table of my practice".
 * 8 columns on desktop, 4 on mobile. Every résumé skill is an element:
 * atomic number, 2-letter symbol, name, family. Family chips dim the
 * non-matching tiles. Entrance is a diagonal wave ((row+col) × 40ms).
 * A sticky inspector shows the real brand logo at 150px (pop animation)
 * or a custom thin line icon, the family, and the work that uses it.
 */
type Tile = Skill & { z: number; delay: number };

export default function Skills() {
  const [filter, setFilter] = useState<SkillFamily | null>(null);
  const [selected, setSelected] = useState<Tile | null>(null);
  const [gridRef, gridIn] = useInView<HTMLDivElement>(0.1);
  const reduced = usePrefersReducedMotion();

  const COLS = 8;
  const tiles: Tile[] = useMemo(
    () =>
      ALL_SKILLS.map((s, i) => ({
        ...s,
        z: i + 1,
        delay: (Math.floor(i / COLS) + (i % COLS)) * 40,
      })),
    []
  );

  const active: Tile = selected ?? tiles[0];

  return (
    <section id="skills" className="section sk" aria-labelledby="skills-h">
      <style>{`
        .sk-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 20px; margin-bottom: 30px; }
        .sk-chips { display: flex; flex-wrap: wrap; gap: 8px; }
        .sk-chip {
          padding: 8px 14px; border-radius: 999px;
          font-family: var(--mono); font-size: 11px; letter-spacing: .04em;
          color: var(--ink-2); background: var(--card);
          box-shadow: inset 0 0 0 1px rgba(13,13,13,.1);
          transition: background .35s var(--ease), color .35s var(--ease), transform .35s var(--ease);
        }
        .sk-chip:hover { transform: translateY(-1px); }
        .sk-chip--on { background: var(--ink); color: var(--paper); }

        .sk-body { display: grid; grid-template-columns: minmax(0,1fr) 320px; gap: clamp(24px, 3.4vw, 48px); align-items: start; }
        @media (max-width: 1080px) { .sk-body { grid-template-columns: 1fr; } .sk-ins { position: static !important; } }

        .sk-grid { display: grid; grid-template-columns: repeat(8, minmax(0,1fr)); gap: 10px; }
        @media (max-width: 1080px) { .sk-grid { grid-template-columns: repeat(6, minmax(0,1fr)); } }
        @media (max-width: 760px)  { .sk-grid { grid-template-columns: repeat(4, minmax(0,1fr)); } }
        @media (max-width: 380px)  { .sk-grid { gap: 7px; } }

        .sk-tile {
          position: relative; aspect-ratio: 1 / 1.06;
          background: var(--card); border-radius: 14px;
          box-shadow: inset 0 0 0 1px rgba(13,13,13,.08);
          display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px;
          padding: 8px 6px; text-align: center;
          opacity: 0; transform: translateY(16px) scale(.92);
          transition: opacity .7s var(--ease), transform .7s var(--ease), box-shadow .4s var(--ease), filter .45s var(--ease);
        }
        .sk-grid.is-in .sk-tile { opacity: 1; transform: none; }
        .sk-tile:hover, .sk-tile:focus-visible { box-shadow: inset 0 0 0 1px rgba(13,13,13,.22), 0 14px 28px -14px rgba(13,13,13,.25); z-index: 2; }
        .sk-tile--dim { filter: grayscale(1) opacity(.22); }
        .sk-tile .z { position: absolute; top: 7px; left: 9px; font-family: var(--mono); font-size: 9px; color: var(--faint); }
        .sk-tile .sy { font-weight: 750; font-size: clamp(17px, 2vw, 24px); letter-spacing: -0.03em; }
        .sk-tile .nm { font-size: clamp(7.6px, .74vw, 9.8px); line-height: 1.25; color: var(--mute); letter-spacing: .01em; }

        .sk-ins { position: sticky; top: 96px; padding: 26px; min-height: 420px; display: flex; flex-direction: column; align-items: center; text-align: center; }
        .sk-ins-logo { width: 150px; height: 150px; display: grid; place-items: center; margin: 8px 0 18px; }
        .sk-ins-logo.pop { animation: skPop .5s var(--ease); }
        @keyframes skPop { 0% { transform: scale(.6); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        .sk-ins h3 { font-size: 21px; font-weight: 700; letter-spacing: -0.03em; margin: 0 0 4px; }
        .sk-ins .fam { font-family: var(--mono); font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--mute); }
        .sk-ins .note { margin-top: 6px; font-size: 13px; color: var(--ink-2); }
        .sk-ins .used { margin-top: 20px; width: 100%; border-top: 1px solid var(--line); padding-top: 16px; }
        .sk-ins .used .lbl { font-family: var(--mono); font-size: 9.5px; letter-spacing: .22em; color: var(--faint); text-transform: uppercase; }
        .sk-ins .used ul { list-style: none; margin: 10px 0 0; padding: 0; display: grid; gap: 7px; }
        .sk-ins .used li { font-size: 12.5px; color: var(--ink-2); line-height: 1.45; }
        .sk-ins .used li .mono { color: var(--faint); margin-right: 7px; font-size: 10px; }
        @media (prefers-reduced-motion: reduce) { .sk-grid .sk-tile { opacity: 1; transform: none; transition: none; } .sk-ins-logo.pop { animation: none; } }
      `}</style>

      <div className="shell">
        <div className="sk-head rv">
          <div>
            <span className="tag">02 — Teaching skills</span>
            <h2 id="skills-h" className="h2" style={{ marginTop: 14, maxWidth: "18ch" }}>
              The periodic table of my <span className="it">practice.</span>
            </h2>
          </div>
          <div className="sk-chips" role="group" aria-label="Filter skills by family">
            <button className={`sk-chip ${filter === null ? "sk-chip--on" : ""}`} onClick={() => setFilter(null)} aria-pressed={filter === null}>All</button>
            {SKILL_GROUPS.map((g) => (
              <button key={g.family} className={`sk-chip ${filter === g.family ? "sk-chip--on" : ""}`} onClick={() => setFilter(g.family)} aria-pressed={filter === g.family}>
                {g.family.replace(" & ", " & ")}
              </button>
            ))}
          </div>
        </div>

        <div className="sk-body">
          <div className={`sk-grid ${gridIn ? "is-in" : ""}`} ref={gridRef} role="list" aria-label="Skills as periodic elements">
            {tiles.map((t) => {
              const dim = filter !== null && t.family !== filter;
              return (
                <button
                  key={`${t.z}-${t.name}`}
                  className={`sk-tile ${dim ? "sk-tile--dim" : ""}`}
                  role="listitem"
                  style={{ transitionDelay: reduced ? "0ms" : `${t.delay}ms` }}
                  onMouseEnter={() => setSelected(t)}
                  onFocus={() => setSelected(t)}
                  onClick={() => setSelected(t)}
                  aria-label={`${t.name} — ${t.family}, element ${t.z}`}
                >
                  <span className="z" aria-hidden="true">{t.z}</span>
                  <span className="sy" aria-hidden="true">{t.symbol}</span>
                  <span className="nm">{t.name}</span>
                </button>
              );
            })}
          </div>

          <aside className="sk-ins card" aria-live="polite" aria-label="Skill inspector">
            <span className="fam">Element № {String(active.z).padStart(2, "0")}</span>
            <div className="sk-ins-logo pop" key={`${active.symbol}-${active.z}`}>
              <TechLogo skill={active} size={isBrand(active) ? 128 : 150} />
            </div>
            <h3>{active.name}</h3>
            <span className="fam">{active.family}</span>
            {active.note && <span className="note">{active.note}</span>}
            <div className="used">
              <span className="lbl">Where it shows up</span>
              <ul>
                {PROJECTS.filter((p) => p.tech.includes(active.name)).map((p) => (
                  <li key={p.id}><span className="mono">{p.index}</span>{p.title}</li>
                ))}
                {PROJECTS.filter((p) => p.tech.includes(active.name)).length === 0 && <li>Across daily classroom practice</li>}
              </ul>
            </div>
          </aside>
        </div>
      </div>
    </section>
  );
}
