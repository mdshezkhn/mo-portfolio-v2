"use client";

import Lenis from "lenis";
import React, { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { prefersReducedMotion } from "./hooks";

interface ScrollApi {
  lenis: Lenis | null;
  scrollToTarget: (target: string | HTMLElement) => void;
}

const ScrollCtx = createContext<ScrollApi>({ lenis: null, scrollToTarget: () => {} });

export const useScroll = () => useContext(ScrollCtx);

/**
 * Lenis smooth scrolling — the only animation dependency of the site.
 * Skipped entirely when the visitor prefers reduced motion; native
 * anchor scrolling is used in that case.
 */
export function ScrollProvider({ children }: { children: React.ReactNode }) {
  const [lenis, setLenis] = useState<Lenis | null>(null);
  const lockRef = useRef(false);

  useEffect(() => {
    if (prefersReducedMotion()) return;
    const l = new Lenis({
      duration: 1.15,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    });
    let raf = 0;
    const loop = (time: number) => { l.raf(time); raf = requestAnimationFrame(loop); };
    raf = requestAnimationFrame(loop);
    setLenis(l);
    return () => { cancelAnimationFrame(raf); l.destroy(); setLenis(null); };
  }, []);

  const scrollToTarget = useCallback(
    (target: string | HTMLElement) => {
      const el = typeof target === "string" ? document.querySelector<HTMLElement>(target) : target;
      if (!el) return;
      if (lenis && !lockRef.current) {
        lenis.scrollTo(el, { offset: 0, duration: 1.2 });
      } else {
        el.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "start" });
      }
    },
    [lenis]
  );

  /** Lock/unlock page scroll (mobile menu). */
  const lockScroll = useCallback(
    (lock: boolean) => {
      lockRef.current = lock;
      if (lenis) { lock ? lenis.stop() : lenis.start(); }
      document.documentElement.style.overflow = lock ? "hidden" : "";
    },
    [lenis]
  );

  return (
    <ScrollCtx.Provider value={{ lenis, scrollToTarget }}>
      <LockCtx.Provider value={lockScroll}>{children}</LockCtx.Provider>
    </ScrollCtx.Provider>
  );
}

const LockCtx = createContext<(lock: boolean) => void>(() => {});
export const useScrollLock = () => useContext(LockCtx);
