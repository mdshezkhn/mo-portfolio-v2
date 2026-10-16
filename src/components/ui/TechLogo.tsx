"use client";

import { ASSET, type Skill } from "@/lib/data";

/**
 * Brand logos keep their official colours (from simple-icons, licence in
 * public/logos/LICENSE) and may carry a very soft brand-tint glow.
 * Concept skills get custom thin line icons in the same spirit — grays only.
 */

export const BRAND: Record<string, { file: string; title: string; tint: string }> = {
  google:     { file: "google.svg",     title: "Google Workspace", tint: "669df6" },
  microsoft:  { file: "microsoft.svg",  title: "Microsoft 365",    tint: "5e5e5e" },
  moodle:     { file: "moodle.svg",     title: "Moodle",           tint: "f98012" },
  canvas:     { file: "canvas.svg",     title: "Canvas",           tint: "e74258" },
  zoom:       { file: "zoom.svg",       title: "Zoom",             tint: "0b5cff" },
  obsstudio:  { file: "obsstudio.svg",  title: "OBS Studio",       tint: "302e31" },
};

export function isBrand(skill: Skill): boolean {
  return Boolean(skill.logo && BRAND[skill.logo]);
}

/* Thin line icons for concept skills — 24×24, stroke 1.5, currentColor. */
const S = { fill: "none", stroke: "currentColor", strokeWidth: 1.5, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };

export const CONCEPT: Record<string, React.ReactNode> = {
  "Primary EAL": <><path {...S} d="M4 5h12v8H8l-4 3z" /><path {...S} d="M9 17h7l4 3v-3" /></>,
  "Multilingual Education": <><circle {...S} cx="12" cy="12" r="8.5" /><path {...S} d="M3.5 12h17M12 3.5c2.6 2.4 2.6 14.6 0 17M12 3.5c-2.6 2.4-2.6 14.6 0 17" /></>,
  "Differentiated Instruction": <><path {...S} d="M12 3l8.5 5-8.5 5-8.5-5z" /><path {...S} d="M3.5 12.5L12 17l8.5-4.5M3.5 16.5L12 21l8.5-4.5" /></>,
  "Formative Assessment": <><path {...S} d="M4 17a8.5 8.5 0 0 1 17 0" /><path {...S} d="M12 17l4.5-5" /><circle cx="12" cy="17" r="1.4" /></>,
  "Literacy Development": <><path {...S} d="M12 6c-2-1.6-4.6-2-8-2v14c3.4 0 6 .4 8 2 2-1.6 4.6-2 8-2V4c-3.4 0-6 .4-8 2z" /><path {...S} d="M12 6v14" /></>,
  "Classroom Management": <><rect {...S} x="3.5" y="3.5" width="7.5" height="7.5" rx="1.5" /><rect {...S} x="13" y="3.5" width="7.5" height="7.5" rx="1.5" /><rect {...S} x="3.5" y="13" width="7.5" height="7.5" rx="1.5" /><rect {...S} x="13" y="13" width="7.5" height="7.5" rx="1.5" /></>,
  "Curriculum Design": <><circle {...S} cx="12" cy="5" r="1.8" /><path {...S} d="M12 6.8V20M12 13l5-4M12 16l-5-4" /></>,
  "Teacher Mentoring": <><circle {...S} cx="8" cy="8" r="3.2" /><path {...S} d="M2.5 20c.7-3.4 2.9-5 5.5-5s4.8 1.6 5.5 5" /><circle {...S} cx="16.5" cy="9" r="2.4" /><path {...S} d="M15.5 14.2c2.7-.3 5 1.3 5.8 4.3" /></>,
  "Professional Development": <><path {...S} d="M3.5 20h5l10-10-5-5-10 10z" /><path {...S} d="M14 5.5l4.5 4.5" /></>,
  "Instructional Quality Assurance": <><path {...S} d="M12 3l7.5 3v6c0 4.5-3.2 7.4-7.5 9-4.3-1.6-7.5-4.5-7.5-9V6z" /><path {...S} d="M8.8 12l2.2 2.2 4.2-4.4" /></>,
  "Assessment Moderation": <><path {...S} d="M12 4v16M5 8h14M7 8l-3 6h6zM17 8l-3 6h6z" /></>,
  "Dialogic Teaching": <><path {...S} d="M3.5 5h9v7h-6l-3 3z" /><path {...S} d="M11.5 16.5h9v-6h-6" /><circle cx="18" cy="16.5" r="1.2" /></>,
  "Questioning Strategies": <><path {...S} d="M4 5h13v8H9l-4 3z" /><path {...S} d="M10.5 12.2a1.8 1.8 0 1 1 .9-3.3 1.8 1.8 0 0 1 .9 3.3v1h-1.8z" /></>,
  "Translanguaging": <><path {...S} d="M4 8.5h13M14 5l3.5 3.5L14 12" /><path {...S} d="M20 15.5H7M10 12l-3.5 3.5L10 19" /></>,
  "Practitioner Research": <><circle {...S} cx="10.5" cy="10.5" r="6.5" /><path {...S} d="M15.5 15.5L21 21" /><path {...S} d="M8 10.5h5M10.5 8v5" /></>,
  "Evidence-Informed Practice": <><path {...S} d="M9 3.5h6M10 3.5v5.2L4.8 18a2 2 0 0 0 1.8 3h10.8a2 2 0 0 0 1.8-3L14 8.7V3.5" /><path {...S} d="M7.5 15h9" /></>,
};

export default function TechLogo({ skill, size = 24, glow = true }: { skill: Skill; size?: number; glow?: boolean }) {
  const brand = skill.logo ? BRAND[skill.logo] : undefined;
  if (brand) {
    return (
      <span
        className="tl-brand"
        style={{
          width: size, height: size, display: "inline-grid", placeItems: "center", borderRadius: size * 0.22,
          boxShadow: glow ? `0 6px ${Math.round(size * 0.55)}px -8px #${brand.tint}66, inset 0 0 0 1px rgba(13,13,13,.06)` : "none",
        }}
      >
        <img src={ASSET(`/logos/${brand.file}`)} alt="" width={Math.round(size * 0.62)} height={Math.round(size * 0.62)} style={{ display: "block" }} />
      </span>
    );
  }
  const icon = CONCEPT[skill.name];
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" aria-hidden="true" style={{ color: "var(--mute)", display: "block" }}>
      {icon ?? <><circle {...S} cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none" /></>}
    </svg>
  );
}
