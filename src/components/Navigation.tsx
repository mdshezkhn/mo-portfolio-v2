"use client";

import { useEffect, useRef, useState } from "react";
import { NAV, PROFILE } from "@/lib/data";
import { usePageScrollProgress } from "@/lib/hooks";
import { useScroll, useScrollLock } from "@/lib/scroll";

/**
 * Fixed top navigation.
 * - Left: round outlined initials mark (solid after 40px, 360° spin on hover) + name (fades on scroll)
 * - Right: pill of links → frosted glass pill once scrolled; ink pill slides under active link
 * - 2px ink scroll-progress bar along the very top
 * - Mobile: "Menu" pill → full-screen paper overlay, clip-path reveal, staggered numbered links, Esc closes
 */
export default function Navigation() {
  const [scrolled, setScrolled] = useState(false);
  const [active, setActive] = useState<string>("");
  const [open, setOpen] = useState(false);
  const [, setTick] = useState(0); // forces indicator re-measure on resize / font load
  const progress = usePageScrollProgress();
  const { scrollToTarget } = useScroll();
  const lockScroll = useScrollLock();
  const rafRef = useRef(0);

  useEffect(() => {
    const onResize = () => setTick((t) => t + 1);
    window.addEventListener("resize", onResize);
    document.fonts?.ready.then(onResize).catch(() => {});
    const t = setTimeout(onResize, 400);
    return () => { window.removeEventListener("resize", onResize); clearTimeout(t); };
  }, []);

  /* frosted state after 40px */
  useEffect(() => {
    const onScroll = () => {
      if (rafRef.current) return;
      rafRef.current = requestAnimationFrame(() => {
        setScrolled(window.scrollY > 40);
        rafRef.current = 0;
      });
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  /* active section tracking */
  useEffect(() => {
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) if (e.isIntersecting) setActive(e.target.id);
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    NAV.forEach(({ id }) => { const el = document.getElementById(id); if (el) io.observe(el); });
    return () => io.disconnect();
  }, []);

  /* Esc closes the mobile menu */
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  useEffect(() => { lockScroll(open); return () => lockScroll(false); }, [open, lockScroll]);

  const go = (id: string) => { setOpen(false); setTimeout(() => scrollToTarget(`#${id}`), open ? 80 : 0); };

  return (
    <>
      <style>{`
        .nv-progress { position: fixed; top: 0; left: 0; height: 2px; background: var(--ink); width: 100%; transform-origin: 0 50%; transform: scaleX(${progress}); z-index: 220; }
        .nv-bar {
          position: fixed; top: 14px; left: 0; right: 0; z-index: 200;
          display: flex; align-items: center; justify-content: space-between;
          padding: 10px var(--gutter);
          pointer-events: none;
        }
        .nv-bar > * { pointer-events: auto; }
        .nv-brand { display: flex; align-items: center; gap: 13px; }
        .nv-mark {
          width: 44px; height: 44px; border-radius: 999px;
          display: grid; place-items: center;
          font-family: var(--mono); font-size: 11px; font-weight: 600; letter-spacing: .06em;
          background: transparent; color: var(--ink);
          box-shadow: inset 0 0 0 1.5px var(--ink);
          transition: background .45s var(--ease), transform .7s var(--ease);
        }
        .nv-mark:hover { transform: rotate(360deg); }
        .nv-mark--solid { background: var(--ink); color: var(--paper); }
        .nv-name {
          font-weight: 650; font-size: 15px; letter-spacing: -0.02em; white-space: nowrap;
          opacity: ${scrolled ? 0 : 1}; transform: translateX(${scrolled ? "-8px" : "0"});
          transition: opacity .5s var(--ease), transform .5s var(--ease);
        }
        .nv-pill {
          display: flex; align-items: center; gap: 2px;
          padding: 5px; border-radius: 999px;
          background: ${scrolled ? "rgba(255,255,255,.72)" : "transparent"};
          backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
          box-shadow: ${scrolled ? "inset 0 0 0 1px rgba(13,13,13,.08), 0 12px 32px -16px rgba(13,13,13,.25)" : "none"};
          transition: background .5s var(--ease), box-shadow .5s var(--ease);
        }
        .nv-link {
          position: relative; z-index: 1;
          padding: 9px 15px; border-radius: 999px;
          font-size: 13.5px; font-weight: 550; letter-spacing: -0.01em; color: var(--ink-2);
          transition: color .4s var(--ease);
          white-space: nowrap;
        }
        .nv-link:hover, .nv-link--active { color: var(--paper); }
        .nv-link--active { z-index: 2; }
        .nv-ind {
          position: absolute; z-index: 0; top: 5px; bottom: 5px;
          background: var(--ink); border-radius: 999px;
          transition: left .55s var(--ease), width .55s var(--ease), opacity .3s var(--ease);
        }
        .nv-menu-btn { display: none; }
        @media (max-width: 900px) {
          .nv-pill { display: none; }
          .nv-menu-btn { display: inline-flex; }
        }
        @media (prefers-reduced-motion: reduce) {
          .nv-mark:hover { transform: none; }
        }
        /* mobile overlay */
        .nv-ov {
          position: fixed; inset: 0; z-index: 210; background: var(--paper);
          clip-path: ${open ? "inset(0 0 0% 0)" : "inset(0 0 100% 0)"};
          transition: clip-path .65s var(--ease);
          display: flex; flex-direction: column; justify-content: center;
          padding: var(--gutter);
        }
        .nv-ov-link {
          display: flex; align-items: baseline; gap: 16px;
          font-size: clamp(34px, 8vw, 56px); font-weight: 700; letter-spacing: -0.045em;
          padding: 10px 0; color: var(--ink);
          opacity: ${open ? 1 : 0}; transform: translateY(${open ? "0" : "22px"});
          transition: opacity .5s var(--ease), transform .6s var(--ease);
          transition-delay: calc(var(--i) * 60ms + 120ms);
        }
        .nv-ov-link .mono { font-size: 13px; color: var(--faint); }
        .nv-ov-close { position: absolute; top: 20px; right: var(--gutter); }
        @media (min-width: 901px) { .nv-ov { display: none; } }
      `}</style>

      <div className="nv-progress" aria-hidden="true" />
      <header className="nv-bar" role="banner">
        <a className="nv-brand" href="#about" onClick={(e) => { e.preventDefault(); go("about"); }} aria-label={`${PROFILE.name} — home`}>
          <span className={`nv-mark ${scrolled ? "nv-mark--solid" : ""}`} aria-hidden="true">{PROFILE.initials}</span>
          <span className="nv-name">{PROFILE.name}</span>
        </a>

        <nav className="nv-pill" aria-label="Sections">
          <span className="nv-ind" style={indicatorStyle(active)} aria-hidden="true" />
          {NAV.map((item) => (
            <a
              key={item.id}
              href={`#${item.id}`}
              data-id={item.id}
              className={`nv-link ${active === item.id ? "nv-link--active" : ""}`}
              aria-current={active === item.id ? "true" : undefined}
              onClick={(e) => { e.preventDefault(); go(item.id); }}
            >
              {item.label}
            </a>
          ))}
        </nav>

        <button className="btn btn--ghost nv-menu-btn" onClick={() => setOpen(true)} aria-expanded={open} aria-controls="mobile-menu">
          Menu
        </button>
      </header>

      <div id="mobile-menu" className="nv-ov" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden={!open}>
        <button className="btn btn--ghost nv-ov-close" onClick={() => setOpen(false)}>Close ✕</button>
        {NAV.map((item) => (
          <a
            key={item.id}
            href={`#${item.id}`}
            className="nv-ov-link"
            style={{ "--i": item.index } as React.CSSProperties}
            onClick={(e) => { e.preventDefault(); go(item.id); }}
            tabIndex={open ? 0 : -1}
          >
            <span className="mono">{item.index}</span> {item.label}
          </a>
        ))}
      </div>
    </>
  );
}

/** Position of the sliding ink pill under the active link. */
function indicatorStyle(active: string): React.CSSProperties {
  if (!active || typeof document === "undefined") return { opacity: 0, left: 0, width: 0 };
  const link = document.querySelector<HTMLAnchorElement>(`.nv-link[data-id="${active}"]`);
  if (!link) return { opacity: 0, left: 0, width: 0 };
  return { opacity: 1, left: link.offsetLeft, width: link.offsetWidth };
}
