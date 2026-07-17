/* ==========================================================
   animations.js
   Handles: header scroll shadow · scroll-reveal entrances
   Fully respects prefers-reduced-motion: .reveal is never
   added when the user has requested reduced motion.
   Part of: Mohammed Shehzad Khan Portfolio v2.0
========================================================== */

export function initAnimations() {
    'use strict';

    /* ── Header shadow on scroll ───────────────────────── */
    /* Adds .is-scrolled when page has scrolled >8px.
       CSS transitions the box-shadow smoothly.
       passive:true keeps this off the main scroll thread. */

    const header = document.querySelector('.site-header');

    if (header) {
        window.addEventListener('scroll', function () {
            header.classList.toggle('is-scrolled', window.scrollY > 8);
        }, { passive: true });
    }

    /* ── Scroll-reveal ─────────────────────────────────── */
    /* If user prefers reduced motion, skip entirely —
       elements stay visible, no layout shift, no hidden
       content. The CSS @media block handles the animation. */

    const prefersReduced = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
    ).matches;

    if (prefersReduced || !('IntersectionObserver' in window)) {
        return;
    }

    /* Add .reveal to the .container inside every section
       except #hero (which uses CSS keyframe animations). */
    const revealTargets = document.querySelectorAll(
        'section:not(#hero) .container'
    );

    if (!revealTargets.length) { return; }

    revealTargets.forEach(function (el) {
        el.classList.add('reveal');
    });

    const revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) { return; }

            entry.target.classList.add('is-visible');
            /* One-shot: unobserve once visible to save resources */
            revealObserver.unobserve(entry.target);
        });
    }, {
        threshold: 0.15
    });

    revealTargets.forEach(function (el) {
        revealObserver.observe(el);
    });
}
