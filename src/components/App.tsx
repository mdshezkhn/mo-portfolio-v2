"use client";

import { useEffect } from "react";
import { ScrollProvider } from "@/lib/scroll";
import Navigation from "./Navigation";
import Hero from "./hero/Hero";
import About from "./sections/About";
import Skills from "./sections/Skills";
import Work from "./sections/Work";
import Certifications from "./sections/Certifications";
import Experience from "./sections/Experience";
import Achievements from "./sections/Achievements";
import Contact from "./sections/Contact";

/**
 * Global RevealObserver — adds .is-in to .rv and .rv-mask elements
 * once, as they enter the viewport. Components never wire this up
 * individually; they just carry the classes and a --i stagger index.
 */
function RevealObserver() {
  useEffect(() => {
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    const watch = () => document.querySelectorAll(".rv:not(.is-in), .rv-mask:not(.is-in)").forEach((el) => io.observe(el));
    watch();
    const mo = new MutationObserver(watch);
    mo.observe(document.body, { childList: true, subtree: true });
    return () => { io.disconnect(); mo.disconnect(); };
  }, []);
  return null;
}

export default function App() {
  return (
    <ScrollProvider>
      <RevealObserver />
      <a
        href="#about"
        style={{ position: "absolute", left: -9999, top: 0 }}
        onFocus={(e) => { e.currentTarget.style.left = "16px"; e.currentTarget.style.top = "16px"; e.currentTarget.style.zIndex = "300"; }}
        onBlur={(e) => { e.currentTarget.style.left = "-9999px"; }}
        className="btn btn--primary"
      >
        Skip to content
      </a>
      <Navigation />
      <main id="main">
        <Hero />
        <About />
        <Skills />
        <Work />
        <Certifications />
        <Experience />
        <Achievements />
        <Contact />
      </main>
    </ScrollProvider>
  );
}
