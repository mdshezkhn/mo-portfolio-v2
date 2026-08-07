/* ==========================================================
   main.js
   Entry point — imports all modules and initialises them
   after the DOM is ready. Uses ES modules (type="module").
   Part of: Mohammed Shehzad Khan Portfolio v2.0

   Stage 4 (2026-07-17): removed the inert theme.js (dark
   mode not in 2A scope) and timeline.js (timeline is CSS-only)
   stubs. Only active modules are imported.
========================================================== */

import { initNavigation } from './navigation.js';
import { initAnimations } from './animations.js';
import { initGallery }    from './gallery.js';
import { initImageFallbacks } from './utilities.js';

document.addEventListener('DOMContentLoaded', function () {
    initNavigation();
    initAnimations();
    initGallery();
    initImageFallbacks();
});
