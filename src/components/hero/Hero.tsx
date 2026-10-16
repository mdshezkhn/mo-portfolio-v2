"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { ASSET, PROFILE } from "@/lib/data";
import { useScroll } from "@/lib/scroll";

/**
 * Hero — the talking-video intro.
 * - Video: 768×960, mix-blend multiply so the white studio background
 *   disappears into the paper page.
 * - Tries to play with sound; falls back to muted autoplay, and unlocks
 *   sound on the visitor's first pointerdown / keydown / touchend.
 * - Pauses (voice stops) once less than 35% of the hero is visible.
 * - Sound toggle: icon-only 46px ink round button (▶ off / ❚❚ on),
 *   soft ping ring while autoplay-with-sound is still blocked.
 * - Placeholder mode: if the hero video files are missing (before the
 *   Google Flow video is generated), a whitened portrait still takes
 *   over the same frame — the layout never breaks.
 */
export default function Hero() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const heroRef = useRef<HTMLElement>(null);
  const [soundOn, setSoundOn] = useState(false);
  const [blocked, setBlocked] = useState(true);
  const [failed, setFailed] = useState(false);   // video files missing → portrait placeholder
  const [started, setStarted] = useState(false);
  const { scrollToTarget } = useScroll();

  /* Play — with sound first, muted as fallback. */
  const tryPlay = useCallback(async (withSound: boolean) => {
    const v = videoRef.current;
    if (!v) return;
    try {
      if (withSound) { v.muted = false; await v.play(); setSoundOn(true); setBlocked(false); }
      else { v.muted = true; await v.play(); }
      setStarted(true);
    } catch {
      v.muted = true;
      try { await v.play(); setStarted(true); } catch { /* not ready yet */ }
      setSoundOn(false);
    }
  }, []);

  /* Initial autoplay attempt once metadata is ready. */
  useEffect(() => {
    const v = videoRef.current;
    if (!v || failed) return;
    const onMeta = () => { void tryPlay(true); };
    v.addEventListener("loadedmetadata", onMeta, { once: true });
    if (v.readyState >= 1) onMeta();
    return () => v.removeEventListener("loadedmetadata", onMeta);
  }, [tryPlay, failed]);

  /* Unlock sound on first interaction (guide behaviour). */
  useEffect(() => {
    const unlock = () => {
      setBlocked(false);
      const v = videoRef.current;
      if (v && !v.muted) return;
      void tryPlay(true);
      window.removeEventListener("pointerdown", unlock);
      window.removeEventListener("keydown", unlock);
      window.removeEventListener("touchend", unlock);
    };
    window.addEventListener("pointerdown", unlock);
    window.addEventListener("keydown", unlock);
    window.addEventListener("touchend", unlock);
    return () => {
      window.removeEventListener("pointerdown", unlock);
      window.removeEventListener("keydown", unlock);
      window.removeEventListener("touchend", unlock);
    };
  }, [tryPlay]);

  /* Pause voice the moment the hero scrolls away (<35% visible). */
  useEffect(() => {
    const v = videoRef.current;
    const el = heroRef.current;
    if (!v || !el || typeof IntersectionObserver === "undefined") return;
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.intersectionRatio >= 0.35) { v.play().catch(() => {}); }
          else { v.pause(); }
        }
      },
      { threshold: [0, 0.35, 0.6, 1] }
    );
    io.observe(el);
    return () => io.disconnect();
  }, [failed]);

  const toggleSound = () => {
    const v = videoRef.current;
    if (!v) return;
    if (v.muted) {
      v.muted = false;
      v.play()
        .then(() => { setSoundOn(true); setBlocked(false); })
        .catch(() => { v.muted = true; setSoundOn(false); setBlocked(true); });
    } else {
      v.muted = true;
      setSoundOn(false);
    }
  };

  return (
    <section
      id="hero"
      ref={heroRef}
      className="hero"
      aria-label="Introduction video"
      style={{ "--started": started ? 1 : 0 } as React.CSSProperties}
    >
      <style>{`
        .hero {
          position: relative;
          min-height: 100svh;
          display: flex; flex-direction: column; align-items: center; justify-content: center;
          padding: 96px var(--gutter) 48px;
          overflow: hidden;
        }
        .hero-ghost {
          position: absolute; inset: 0;
          display: grid; place-items: center;
          font-weight: 800; font-size: clamp(120px, 24vw, 380px);
          letter-spacing: -0.02em; line-height: 1; text-transform: uppercase;
          color: transparent;
          -webkit-text-stroke: 1px rgba(13,13,13,.10);
          user-select: none; pointer-events: none;
          white-space: nowrap;
        }
        .hero-frame {
          position: relative;
          height: min(84svh, 980px);
          aspect-ratio: 768 / 960;
          max-width: 100%;
          display: grid; place-items: end center;
        }
        @media (max-width: 700px) { .hero-frame { height: 62svh; } }
        .hero-frame video, .hero-frame img {
          height: 100%; width: 100%; object-fit: cover;
          mix-blend-mode: multiply; /* white studio background melts into the paper */
          opacity: 0; transition: opacity 1.2s var(--ease);
        }
        .hero[data-started="1"] .hero-frame video, .hero-frame img.hero-img { opacity: 1; }
        .hero-img { animation: heroFloat 7s ease-in-out infinite; }
        @keyframes heroFloat { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-10px) } }
        .hero-copy {
          position: relative; z-index: 2;
          display: flex; flex-direction: column; align-items: center; gap: 22px;
          text-align: center; margin-top: 6px;
        }
        .hero-title {
          font-size: clamp(30px, 4.4vw, 54px); font-weight: 700;
          letter-spacing: -0.045em; line-height: 1.04;
          max-width: 16ch;
        }
        .hero-ctas { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
        .hero-sound {
          position: absolute; right: 22px; bottom: 26px; z-index: 5;
          width: 46px; height: 46px; border-radius: 999px;
          background: var(--ink); color: var(--paper);
          display: ${failed ? "none" : "grid"}; place-items: center;
          font-size: 13px; letter-spacing: .04em;
          transition: transform .35s var(--ease);
        }
        .hero-sound:hover { transform: translateY(-2px); }
        .hero-sound .ping {
          position: absolute; inset: -7px; border-radius: 999px;
          box-shadow: 0 0 0 0 rgba(13,13,13,.45);
          animation: heroPing 1.6s var(--ease) infinite;
          display: ${blocked && !soundOn ? "block" : "none"};
        }
        @keyframes heroPing { 0% { box-shadow: 0 0 0 0 rgba(13,13,13,.4); } 100% { box-shadow: 0 0 0 18px rgba(13,13,13,0); } }
        .hero-tag { position: absolute; top: 86px; left: var(--gutter); }
        @media (max-width: 900px) { .hero-tag { display: none; } }
        @media (prefers-reduced-motion: reduce) { .hero-img { animation: none; } .hero-sound .ping { display: none; } }
      `}</style>

      <span className="tag hero-tag" aria-hidden="true">00 — Hello</span>
      <div className="hero-ghost" aria-hidden="true">{PROFILE.firstName}</div>

      <div className="hero-frame">
        {failed ? (
          <img
            className="hero-img"
            src={ASSET("/hero/placeholder.webp")}
            alt={`${PROFILE.name} standing against a plain white background`}
          />
        ) : (
          <video
            ref={videoRef}
            muted
            loop
            playsInline
            preload="auto"
            aria-label={`Intro: ${PROFILE.name} introduces himself`}
            onError={() => setFailed(true)}
          >
            <source src={ASSET("/hero/hero.webm")} type="video/webm" onError={() => {}} />
            <source src={ASSET("/hero/hero.mp4")} type="video/mp4" onError={() => setFailed(true)} />
          </video>
        )}
      </div>

      <div className="hero-copy">
        <h1 className="hero-title rv">
          International Primary <span className="it">EAL</span> Educator.
        </h1>
        <div className="hero-ctas rv" style={{ "--i": 1 } as React.CSSProperties}>
          <a className="btn btn--primary" href="#work" onClick={(e) => { e.preventDefault(); scrollToTarget("#work"); }}>
            Explore work
          </a>
          <a className="btn btn--ghost" href="#contact" onClick={(e) => { e.preventDefault(); scrollToTarget("#contact"); }}>
            Let&rsquo;s talk
          </a>
          <a className="btn btn--ghost" href={ASSET(PROFILE.resumePath)} download>
            Résumé ↓
          </a>
        </div>
      </div>

      <button className="hero-sound" onClick={toggleSound} aria-label={soundOn ? "Mute intro sound" : "Unmute intro sound"}>
        <span className="ping" aria-hidden="true" />
        <span aria-hidden="true">{soundOn ? "❚❚" : "▶"}</span>
      </button>
    </section>
  );
}
