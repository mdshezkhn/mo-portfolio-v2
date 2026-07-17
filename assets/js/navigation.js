/* ==========================================================
   navigation.js
   Handles: mobile menu toggle · outside-click close ·
            Escape key close · active-section highlighting
   Does not use any framework or build tool.
   Part of: Mohammed Shehzad Khan Portfolio v2.0
========================================================== */

export function initNavigation() {
    'use strict';

    const toggle   = document.getElementById('nav-toggle');
    const menu     = document.getElementById('nav-menu');

    if (!toggle || !menu) { return; }

    const navLinks = menu.querySelectorAll('a');

    /* ── State helpers ─────────────────────────────────── */

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

    /* ── Toggle on button click ────────────────────────── */

    toggle.addEventListener('click', function () {
        isOpen() ? closeMenu() : openMenu();
    });

    /* ── Close when a nav link is clicked ─────────────── */

    navLinks.forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });

    /* ── Close on outside click ────────────────────────── */

    document.addEventListener('click', function (e) {
        if (isOpen() && !e.target.closest('.site-header')) {
            closeMenu();
        }
    });

    /* ── Close on Escape key, return focus to toggle ───── */
    /* Required by ARIA APG disclosure navigation pattern   */

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && isOpen()) {
            closeMenu();
            toggle.focus();
        }
    });

    /* ── Active section highlighting ───────────────────── */
    /* Sets aria-current="page" on the nav link matching
       whichever section occupies the centre of the screen. */

    const sections = document.querySelectorAll('main section[id]');

    if (!('IntersectionObserver' in window) || !sections.length) { return; }

    const sectionObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) { return; }

            navLinks.forEach(function (link) {
                link.removeAttribute('aria-current');
            });

            const active = menu.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) {
                active.setAttribute('aria-current', 'page');
            }
        });
    }, {
        rootMargin: '-40% 0px -55% 0px'
    });

    sections.forEach(function (section) {
        sectionObserver.observe(section);
    });
}
