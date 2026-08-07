/* ==========================================================
   gallery.js
   Classroom Moments: category filtering + an accessible
   lightbox (Esc to close, ←/→ to navigate, click backdrop
   to dismiss, focus returns to the trigger). Progressive
   enhancement — without JS the grid still shows every image.
   Respects missing assets: if an <img> failed to load (the
   .img-fallback placeholder took its place), the lightbox
   shows the caption only rather than a broken image.
   Part of: Mohammed Shehzad Khan Portfolio v2.0
========================================================== */

export function initGallery() {
    'use strict';

    const gallery = document.querySelector('[data-gallery]');
    if (!gallery) { return; }

    const filters = Array.from(gallery.querySelectorAll('.gallery-filter'));
    const items   = Array.from(gallery.querySelectorAll('.gallery-item'));
    const emptyMsg = gallery.querySelector('.gallery-empty');

    /* ── Filtering ───────────────────────────────────────── */
    filters.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const filter = btn.dataset.filter;

            filters.forEach(function (b) {
                const active = b === btn;
                b.classList.toggle('is-active', active);
                b.setAttribute('aria-pressed', active ? 'true' : 'false');
            });

            let visible = 0;
            items.forEach(function (item) {
                const show = filter === 'all' || item.dataset.category === filter;
                item.classList.toggle('is-hidden', !show);
                if (show) { visible++; }
            });

            if (emptyMsg) { emptyMsg.hidden = visible !== 0; }
        });
    });

    /* ── Lightbox ───────────────────────────────────────── */
    const figures = items.map(function (item) {
        return item.querySelector('figure');
    });
    let current = -1;
    let lastFocused = null;

    const overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.hidden = true;
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Classroom image viewer');
    overlay.innerHTML =
        '<button type="button" class="lightbox__btn lightbox__close" aria-label="Close image viewer">×</button>' +
        '<button type="button" class="lightbox__btn lightbox__prev" aria-label="Previous image">‹</button>' +
        '<button type="button" class="lightbox__btn lightbox__next" aria-label="Next image">›</button>' +
        '<figure class="lightbox__figure">' +
            '<img class="lightbox__img" alt="">' +
            '<figcaption class="lightbox__caption"></figcaption>' +
        '</figure>';
    document.body.appendChild(overlay);

    const lbImg = overlay.querySelector('.lightbox__img');
    const lbCap = overlay.querySelector('.lightbox__caption');
    const btnClose = overlay.querySelector('.lightbox__close');
    const btnPrev  = overlay.querySelector('.lightbox__prev');
    const btnNext  = overlay.querySelector('.lightbox__next');

    function show(index) {
        current = (index + figures.length) % figures.length;
        const fig = figures[current];
        const img = fig.querySelector('img');
        const cap = fig.querySelector('figcaption');

        const usable = img && !(img.complete && img.naturalWidth === 0);
        if (usable) {
            lbImg.style.display = '';
            lbImg.src = img.currentSrc || img.src;
            lbImg.alt = img.alt;
        } else {
            lbImg.removeAttribute('src');
            lbImg.alt = '';
            lbImg.style.display = 'none';
        }

        lbCap.textContent = (cap && cap.textContent)
            ? cap.textContent
            : (usable ? '' : 'Image will appear here once supplied.');

        overlay.hidden = false;
        document.body.style.overflow = 'hidden';
        btnClose.focus();
    }

    function hide() {
        overlay.hidden = true;
        document.body.style.overflow = '';
        if (lastFocused && typeof lastFocused.focus === 'function') {
            lastFocused.focus();
        }
    }

    figures.forEach(function (fig, i) {
        fig.setAttribute('tabindex', '0');
        fig.setAttribute('role', 'button');
        const img = fig.querySelector('img');
        fig.setAttribute(
            'aria-label',
            'View image: ' + (img ? img.alt : 'classroom moment')
        );

        fig.addEventListener('click', function () {
            lastFocused = document.activeElement;
            show(i);
        });
        fig.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                lastFocused = document.activeElement;
                show(i);
            }
        });
    });

    btnClose.addEventListener('click', hide);
    btnPrev.addEventListener('click', function () { show(current - 1); });
    btnNext.addEventListener('click', function () { show(current + 1); });
    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) { hide(); }
    });
    document.addEventListener('keydown', function (e) {
        if (overlay.hidden) { return; }
        if (e.key === 'Escape') { hide(); }
        else if (e.key === 'ArrowLeft') { show(current - 1); }
        else if (e.key === 'ArrowRight') { show(current + 1); }
    });
}
