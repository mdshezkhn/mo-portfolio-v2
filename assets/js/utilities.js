/* ==========================================================
   utilities.js
   Small progressive-enhancement helpers.
   Part of: Mohammed Shehzad Khan Portfolio v2.0
========================================================== */

/* ── Image fallback ────────────────────────────────────── */
/* If an <img> fails to load (e.g. an asset not yet supplied),
   replace it with a styled placeholder so the layout stays
   intact and no broken-image icon appears. Present images are
   left untouched. Runs only in browsers with JS; without JS the
   native broken-image state is the (rare) degraded case. */

export function initImageFallbacks() {
    'use strict';

    const images = document.querySelectorAll('img');

    images.forEach(function (img) {
        function showFallback() {
            if (!img.parentNode || img.dataset.fallbackApplied) { return; }
            img.dataset.fallbackApplied = 'true';

            const fallback = document.createElement('div');
            fallback.className = 'img-fallback';
            fallback.setAttribute('role', 'img');
            fallback.setAttribute('aria-label', img.getAttribute('alt') || 'Image');

            const label = img.getAttribute('alt') || 'Image';
            fallback.innerHTML =
                '<svg class="img-fallback__icon" viewBox="0 0 24 24" ' +
                'width="28" height="28" fill="none" stroke="currentColor" ' +
                'stroke-width="1.6" aria-hidden="true">' +
                '<rect x="3" y="3" width="18" height="18" rx="2"/>' +
                '<circle cx="8.5" cy="8.5" r="1.5"/>' +
                '<path d="M21 15l-5-5L5 21"/></svg>' +
                '<span class="img-fallback__label">' + label + '</span>';

            img.parentNode.replaceChild(fallback, img);
        }

        /* Catch images that already failed before this script ran */
        if (img.complete && img.naturalWidth === 0) {
            showFallback();
        } else {
            img.addEventListener('error', showFallback);
        }
    });
}
