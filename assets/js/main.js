/* ==========================================================
   main.js — Navigation
   Handles: mobile menu toggle · outside-click close ·
            Escape key close · active-section highlighting
   Does not use any framework or build tool.
========================================================== */

(function () {
    'use strict';

    /* ── Element references ───────────────────────────────── */

    var toggle   = document.getElementById('nav-toggle');
    var menu     = document.getElementById('nav-menu');

    /* Guard: bail out silently if elements are absent */
    if (!toggle || !menu) { return; }

    var navLinks = menu.querySelectorAll('a');

    /* ── State helpers ────────────────────────────────────── */

    function isOpen() {
        return menu.classList.contains('is-open');
    }

    function openMenu() {
        menu.classList.add('is-open');
        toggle.setAttribute('aria-expanded', 'true');
        toggle.setAttribute('aria-label', 'Close navigation menu');
    }

    function closeMenu() {
        menu.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open navigation menu');
    }

    /* ── Toggle on button click ───────────────────────────── */

    toggle.addEventListener('click', function () {
        if (isOpen()) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    /* ── Close when a nav link is clicked ────────────────── */
    /*    Keeps the menu from covering the destination section */

    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            closeMenu();
        });
    });

    /* ── Close on outside click ───────────────────────────── */
    /*    .closest() returns null if click is outside header   */

    document.addEventListener('click', function (e) {
        if (isOpen() && !e.target.closest('.site-header')) {
            closeMenu();
        }
    });

    /* ── Close on Escape key, return focus to toggle ─────── */
    /*    Required by ARIA APG disclosure navigation pattern   */

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && isOpen()) {
            closeMenu();
            toggle.focus();
        }
    });

    /* ── Active section highlighting ──────────────────────── */
    /*    Sets aria-current="page" on the nav link matching    */
    /*    whichever section occupies the centre of the screen. */
    /*    CSS rule .nav-links a[aria-current="page"] colours   */
    /*    the active link with the accent colour.              */

    var sections = document.querySelectorAll('main section[id]');

    if ('IntersectionObserver' in window && sections.length) {

        var sectionObserver = new IntersectionObserver(function (entries) {

            entries.forEach(function (entry) {

                if (!entry.isIntersecting) { return; }

                /* Clear current from all links */
                navLinks.forEach(function (link) {
                    link.removeAttribute('aria-current');
                });

                /* Mark the link whose href matches the visible section */
                var active = menu.querySelector(
                    'a[href="#' + entry.target.id + '"]'
                );
                if (active) {
                    active.setAttribute('aria-current', 'page');
                }

            });

        }, {
            /* Section must be in the 40-55% band of the viewport */
            rootMargin: '-40% 0px -55% 0px'
        });

        sections.forEach(function (section) {
            sectionObserver.observe(section);
        });

    }

}());

/* ==========================================================
   main.js — Animations
   Handles: header scroll shadow · scroll-reveal entrances
   Fully respects prefers-reduced-motion at the JS level:
   the .reveal class (which hides elements) is never added
   when the user has requested reduced motion.
========================================================== */

(function () {
    'use strict';

    /* -- Header shadow on scroll ----------------------------- */
    /*    Adds .is-scrolled when page has scrolled > 8px.     */
    /*    CSS transitions the box-shadow smoothly.            */
    /*    passive:true keeps this off the main scroll thread. */

    var header = document.querySelector('.site-header');

    if (header) {

        window.addEventListener('scroll', function () {

            if (window.scrollY > 8) {
                header.classList.add('is-scrolled');
            } else {
                header.classList.remove('is-scrolled');
            }

        }, { passive: true });

    }

    /* -- Scroll-reveal --------------------------------------- */

    /* Check motion preference at the JS level. If the user   */
    /* prefers reduced motion, skip adding .reveal entirely -- */
    /* elements stay visible, no layout shift, no hidden      */
    /* content. The CSS @media block handles the animation.   */

    var prefersReduced = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
    ).matches;

    if (prefersReduced || !('IntersectionObserver' in window)) {
        return;
    }

    /* Add .reveal to the .container inside every section     */
    /* except #hero (which uses CSS keyframe animations).     */

    var revealTargets = document.querySelectorAll(
        'section:not(#hero) .container'
    );

    if (!revealTargets.length) { return; }

    revealTargets.forEach(function (el) {
        el.classList.add('reveal');
    });

    var revealObserver = new IntersectionObserver(function (entries) {

        entries.forEach(function (entry) {

            if (!entry.isIntersecting) { return; }

            entry.target.classList.add('is-visible');

            /* One-shot: unobserve once visible to save resources */
            revealObserver.unobserve(entry.target);

        });

    }, {
        /* Fire when 15% of the element is visible */
        threshold: 0.15
    });

    revealTargets.forEach(function (el) {
        revealObserver.observe(el);
    });

}());
