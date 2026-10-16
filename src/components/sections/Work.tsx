"use client";

import { useState } from "react";
import { ALL_SKILLS, PROJECTS } from "@/lib/data";
import TechLogo from "../ui/TechLogo";

/**
 * Work — expanding accordion gallery.
 * One tall panel per résumé contribution (min(78svh, 600px)); hover,
 * focus or tap opens it wide (flex 8) while the others fold into slim
 * spines carrying number, vertical title and a rotating "+" button.
 * The open panel pairs the résumé text with a grayscale illustrative
 * mini-UI (pure CSS/JSX, labelled so it is never mistaken for a
 * screenshot). On mobile the panels become a vertical accordion.
 */
export default function Work() {
  const [open, setOpen] = useState(0);

  return (
    <section id="work" className="section wk" aria-labelledby="work-h">
      <style>{`
        .wk-head { margin-bottom: 34px; }
        .wk-row { display: flex; gap: 12px; height: min(78svh, 600px); }
        .wk-panel {
          position: relative; flex: 1; overflow: hidden;
          border-radius: 26px; background: var(--card);
          box-shadow: inset 0 0 0 1px rgba(13,13,13,.08);
          transition: flex 0.85s var(--ease), box-shadow .6s var(--ease);
          display: flex; flex-direction: column;
        }
        .wk-panel--open { flex: 8; box-shadow: inset 0 0 0 1px rgba(13,13,13,.1), 0 30px 60px -30px rgba(13,13,13,.3); }

        /* spine (closed state) */
        .wk-spine {
          position: absolute; inset: 0;
          display: flex; flex-direction: column; align-items: center; justify-content: space-between;
          padding: 22px 0 18px;
          opacity: 1; transition: opacity .5s var(--ease);
        }
        .wk-panel--open .wk-spine { opacity: 0; pointer-events: none; }
        .wk-spine .no { font-family: var(--mono); font-size: 12px; color: var(--mute); }
        .wk-spine .vt {
          writing-mode: vertical-rl; transform: rotate(180deg);
          font-weight: 650; font-size: 16.5px; letter-spacing: -0.02em; color: var(--ink-2);
          white-space: nowrap; max-height: 62%;
          overflow: hidden; text-overflow: ellipsis;
        }
        .wk-plus {
          width: 34px; height: 34px; border-radius: 999px;
          display: grid; place-items: center;
          box-shadow: inset 0 0 0 1px rgba(13,13,13,.18);
          font-size: 17px; color: var(--ink-2);
          transition: transform .6s var(--ease), background .4s var(--ease), color .4s var(--ease);
        }
        .wk-panel:hover .wk-plus { transform: rotate(90deg); background: var(--ink); color: var(--paper); }

        /* open content */
        .wk-body {
          position: absolute; inset: 0;
          display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, .95fr); gap: clamp(18px, 2.6vw, 44px);
          padding: clamp(22px, 3vw, 42px);
          opacity: 0; transform: translateY(12px);
          transition: opacity .55s var(--ease) .18s, transform .6s var(--ease) .18s;
        }
        .wk-panel--open .wk-body { opacity: 1; transform: none; }
        .wk-kicker { font-family: var(--mono); font-size: 10.5px; letter-spacing: .18em; text-transform: uppercase; color: var(--mute); }
        .wk-no { font-family: var(--mono); font-size: 12px; color: var(--faint); margin-bottom: 10px; display: block; }
        .wk-title { font-size: clamp(21px, 2.1vw, 30px); font-weight: 700; letter-spacing: -0.04em; line-height: 1.08; margin: 6px 0 12px; }
        .wk-desc { color: var(--ink-2); font-size: 14.5px; line-height: 1.7; max-width: 52ch; }
        .wk-feats { list-style: none; margin: 18px 0 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 9px 18px; }
        @media (max-width: 700px) { .wk-feats { grid-template-columns: 1fr; } }
        .wk-feats li { font-size: 12.8px; color: var(--mute); line-height: 1.5; padding-left: 15px; position: relative; }
        .wk-feats li::before { content: ""; position: absolute; left: 0; top: .62em; width: 6px; height: 6px; border-radius: 2px; background: var(--soft); box-shadow: inset 0 0 0 1px rgba(13,13,13,.3); }
        .wk-tech { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }

        .wk-ui { position: relative; border-radius: 18px; background: #fafaf8; box-shadow: inset 0 0 0 1px rgba(13,13,13,.09); overflow: hidden;
                 clip-path: inset(0 100% 0 0); transition: clip-path 1s var(--ease) .25s; }
        .wk-panel--open .wk-ui { clip-path: inset(0 0 0 0); }
        .wk-ui .lab { position: absolute; top: 12px; right: 14px; z-index: 3; font-family: var(--mono); font-size: 9px; letter-spacing: .16em; text-transform: uppercase; color: var(--faint); background: rgba(255,255,255,.8); padding: 4px 8px; border-radius: 999px; box-shadow: inset 0 0 0 1px rgba(13,13,13,.1); }

        .mU { padding: 26px 22px; display: flex; flex-direction: column; gap: 12px; height: 100%; color: #3a3a3a; }
        .mU-bar { height: 8px; border-radius: 99px; background: #ececec; box-shadow: inset 0 0 0 1px rgba(13,13,13,.07); overflow: hidden; }
        .mU-bar i { display: block; height: 100%; border-radius: 99px; background: #c9c9c9; }
        .mU-card { border-radius: 12px; background: #fff; box-shadow: inset 0 0 0 1px rgba(13,13,13,.08); padding: 12px 14px; display: grid; gap: 8px; }
        .mU-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
        .mU-h { font-family: var(--mono); font-size: 9px; letter-spacing: .18em; text-transform: uppercase; color: #9a9a9a; }
        .mU-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; flex: 1; }
        .mU-col { border-radius: 12px; background: #fff; box-shadow: inset 0 0 0 1px rgba(13,13,13,.08); padding: 10px; display: grid; gap: 8px; align-content: start; }
        .mU-chip { height: 26px; border-radius: 8px; background: #f1f1f1; box-shadow: inset 0 0 0 1px rgba(13,13,13,.06); }
        .mU-avatar { width: 40px; height: 40px; border-radius: 999px; background: #e6e6e6; box-shadow: inset 0 0 0 1px rgba(13,13,13,.12); }

        @media (max-width: 900px) {
          .wk-row { flex-direction: column; height: auto; }
          .wk-panel { flex: none; min-height: 64px; transition: min-height .8s var(--ease); }
          .wk-panel--open { min-height: 720px; flex: none; }
          .wk-spine { position: relative; flex-direction: row; padding: 20px 20px; }
          .wk-spine .vt { writing-mode: horizontal-tb; transform: none; max-height: none; flex: 1; text-align: left; }
          .wk-body { position: absolute; grid-template-columns: 1fr; overflow-y: auto; }
        }
        @media (prefers-reduced-motion: reduce) {
          .wk-panel { transition: none; }
          .wk-panel--open { flex: 8; }
          .wk-ui { transition: none; clip-path: inset(0 0 0 0); }
        }
      `}</style>

      <div className="shell">
        <div className="wk-head rv">
          <span className="tag">03 — Selected work</span>
          <h2 id="work-h" className="h2" style={{ marginTop: 14, maxWidth: "20ch" }}>
            Leadership, out of the <span className="it">classroom.</span>
          </h2>
        </div>

        <div className="wk-row rv" style={{ "--i": 1 } as React.CSSProperties}>
          {PROJECTS.map((p, i) => (
            <article
              key={p.id}
              className={`wk-panel ${open === i ? "wk-panel--open" : ""}`}
              tabIndex={0}
              role="button"
              aria-expanded={open === i}
              aria-controls={`${p.id}-body`}
              onMouseEnter={() => setOpen(i)}
              onFocus={() => setOpen(i)}
              onClick={() => setOpen(i)}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setOpen(i); } }}
              aria-label={`Project ${p.index}: ${p.title}`}
            >
              {/* closed spine */}
              <div className="wk-spine" aria-hidden={open === i}>
                <span className="no">{p.index}</span>
                <span className="vt">{p.title}</span>
                <span className="wk-plus">+</span>
              </div>

              {/* open body */}
              <div className="wk-body" id={`${p.id}-body`} aria-hidden={open !== i}>
                <div>
                  <span className="wk-no">{p.index} / 05</span>
                  <span className="wk-kicker">{p.kicker}</span>
                  <h3 className="wk-title">{p.title}</h3>
                  <p className="wk-desc">{p.description}</p>
                  <ul className="wk-feats">
                    {p.features.map((f) => <li key={f}>{f}</li>)}
                  </ul>
                  <div className="wk-tech">
                    {p.tech.map((name) => {
                      const skill = ALL_SKILLS.find((s) => s.name === name);
                      return skill ? (
                        <span className="chip" key={name}>
                          <TechLogo skill={skill} size={15} glow={false} />
                          {name}
                        </span>
                      ) : null;
                    })}
                  </div>
                </div>
                <div className="wk-ui" aria-hidden="true">
                  <span className="lab">Illustrative UI</span>
                  <MiniUI kind={p.ui} />
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

/* Grayscale mini-UIs — hints at the product, never a real screenshot. */
function MiniUI({ kind }: { kind: Project["ui"] }) {
  if (kind === "workshops") {
    return (
      <div className="mU">
        <div className="mU-row"><span className="mU-h">PD programme — Q3</span><span className="mU-h">3 campuses</span></div>
        <div className="mU-grid">
          {[
            { t: "Assessment rigour", v: 86 },
            { t: "QA frameworks", v: 72 },
            { t: "Mentoring clinics", v: 64 },
          ].map((c) => (
            <div className="mU-card" key={c.t}>
              <span className="mU-h">{c.t}</span>
              <div className="mU-bar"><i style={{ width: `${c.v}%` }} /></div>
              <span className="mU-h">delivered</span>
            </div>
          ))}
        </div>
        <div className="mU-row"><span className="mU-h">UK · Dubai · Malta</span><span className="mU-h">◉ live session</span></div>
      </div>
    );
  }
  if (kind === "programmes") {
    return (
      <div className="mU">
        <div className="mU-row"><span className="mU-h">Training pipeline</span><span className="mU-h">distributed teams</span></div>
        <div className="mU-grid">
          {["Design", "Coach", "Deploy"].map((col, ci) => (
            <div className="mU-col" key={col}>
              <span className="mU-h">{col}</span>
              {Array.from({ length: 3 - ci > 1 ? 2 : 1 }).map((_, k) => <div key={k} className="mU-chip" style={{ opacity: 1 - k * 0.25 }} />)}
            </div>
          ))}
        </div>
        <div className="mU-bar"><i style={{ width: "68%" }} /></div>
      </div>
    );
  }
  if (kind === "mentoring") {
    return (
      <div className="mU">
        <div className="mU-card">
          <div className="mU-row">
            <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <span className="mU-avatar" />
              <div><div style={{ width: 84, height: 9, borderRadius: 9, background: "#e3e3e3" }} /><div style={{ width: 54, height: 7, borderRadius: 9, background: "#efefef", marginTop: 6 }} /></div>
            </div>
            <span className="mU-h">induction yr 1</span>
          </div>
          <div className="mU-bar"><i style={{ width: "78%" }} /></div>
        </div>
        {["Classroom routines", "Growth-plan review", "Co-teaching sync"].map((t, i) => (
          <div className="mU-card" key={t}>
            <div className="mU-row"><span style={{ fontSize: 11.5, color: "#555" }}>{t}</span><span className="mU-h">{["✓", "◐", "·"][i]}</span></div>
            <div className="mU-bar"><i style={{ width: `${[92, 55, 30][i]}%` }} /></div>
          </div>
        ))}
      </div>
    );
  }
  if (kind === "moderation") {
    return (
      <div className="mU">
        <div className="mU-row"><span className="mU-h">Grade 5 · writing moderation</span><span className="mU-h">4 teams</span></div>
        {[
          { c: "Task response", a: 88, b: 91 },
          { c: "Language accuracy", a: 74, b: 76 },
          { c: "Moderation agreement", a: 96, b: 97 },
        ].map((r) => (
          <div className="mU-card" key={r.c}>
            <div className="mU-row"><span style={{ fontSize: 11.5, color: "#555" }}>{r.c}</span><span className="mU-h">team A · team B</span></div>
            <div className="mU-bar"><i style={{ width: `${r.a}%` }} /></div>
            <div className="mU-bar"><i style={{ width: `${r.b}%`, background: "#dedede" }} /></div>
          </div>
        ))}
        <div className="mU-row"><span className="mU-h">calibrated ✓</span><span className="mU-h">signed off</span></div>
      </div>
    );
  }
  return (
    <div className="mU">
      <div className="mU-row"><span className="mU-h">Demo lesson — early years</span><span className="mU-h">◈ modelling</span></div>
      <div className="mU-grid" style={{ gridTemplateColumns: "1fr 1fr" }}>
        <div className="mU-col">
          <span className="mU-h">Warm-up</span>
          <div className="mU-chip" /><div className="mU-chip" />
          <span className="mU-h">story circle</span>
        </div>
        <div className="mU-col">
          <span className="mU-h">Practice</span>
          <div className="mU-chip" />
          <span className="mU-h">pair talk</span>
          <div className="mU-chip" />
        </div>
      </div>
      <div className="mU-card">
        <div className="mU-row"><span style={{ fontSize: 11.5, color: "#555" }}>Coaching debrief</span><span className="mU-h">▶ 12 min</span></div>
        <div className="mU-bar"><i style={{ width: "44%" }} /></div>
      </div>
    </div>
  );
}

type Project = (typeof PROJECTS)[number];
