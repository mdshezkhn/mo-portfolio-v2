/* ==========================================================
   animations.js
   Handles: header scroll shadow · scroll-reveal entrances
   Fully respects prefers-reduced-motion.
   Part of: Mohammed Shehzad Khan Portfolio v3
========================================================== */

export function initAnimations() {
    'use strict';

    /* ── Header shadow on scroll ────────────────── */
    /* Adds .is-scrolled when page has scrolled >8px.
       CSS transitions the box-shadow smoothly.
       passive:true keeps this off the main scroll thread. */

    const header = document.querySelector('.site-header');

    if (header) {
        window.addEventListener('scroll', function () {
            header.classList.toggle('is-scrolled', window.scrollY > 8);
        }, { passive: true });
    }

    /* ── Scroll-reveal ──────────────────────────── */
    /* SAFETY-NET MECHANISM (Phase 1.2 fix).
       Content is visible by DEFAULT. Only a JS-added
       js-reveal-ready class may hide-then-reveal. This
       guarantees that no section can remain hidden on
       mobile — the worst case is a section that fades in
       slightly later, never a section that never appears. */

    const prefersReduced = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
    ).matches;

    /* If reduced motion, leave everything visible — no
       reveal class is ever added. */
    if (prefersReduced) { return; }

    /* IntersectionObserver is optional. If absent, the
       load-time force-reveal below still runs, so the
       page is fully readable without JS. */
    if (!('IntersectionObserver' in window)) { return; }

    /* Reveal targets: every section container except #hero
       (which uses its own keyframe entrance). */
    const revealTargets = document.querySelectorAll(
        'section:not(#hero) .container'
    );

    if (!revealTargets.length) { return; }

    /* Step 1: mark targets as reveal-ready. The CSS hidden
       state is gated on .js-reveal-ready, so this is the
       ONLY class that may hide content. */
    revealTargets.forEach(function (el) {
        el.classList.add('js-reveal-ready');
    });

    /* Step 2: observe with a generous rootMargin so elements
       enter the viewport early (mobile scroll is fast and
       erratic — we never want a target to sit just outside
       the margin and never trigger). threshold:0 means
       even a 1px sliver counts as intersecting. */
    const revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) { return; }
            entry.target.classList.add('js-reveal-visible');
            revealObserver.unobserve(entry.target);
        });
    }, {
        threshold: 0,
        rootMargin: '80px 0px 0px 0px'
    });

    revealTargets.forEach(function (el) {
        revealObserver.observe(el);
    });

    /* Step 3: FALLBACK TIMER. A slow network, a stalled
       renderer, or a slow first paint can prevent the
       observer from ever firing. After 3 seconds we
       force-reveal every target unconditionally. */
    const fallbackTimer = window.setTimeout(function () {
        revealTargets.forEach(function (el) {
            el.classList.add('js-reveal-visible');
        });
    }, 3000);

    /* Step 4: window.load force-reveal. If the page finishes
       loading and any target is still hidden, reveal it.
       This catches anchor jumps (direct #section links)
       where the observer never gets a chance to fire. */
    function forceRevealOnLoad() {
        revealTargets.forEach(function (el) {
            el.classList.add('js-reveal-visible');
        });
        window.clearTimeout(fallbackTimer);
    }

    if (document.readyState === 'complete') {
        forceRevealOnLoad();
    } else {
        window.addEventListener('load', forceRevealOnLoad, { once: true });
    }
}
