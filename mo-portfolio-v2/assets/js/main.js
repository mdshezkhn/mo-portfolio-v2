/* ==========================================================
   main.js
   Entry point — imports all modules and initialises them
   after the DOM is ready. Uses ES modules (type="module").
   Part of: Mohammed Shehzad Khan Portfolio v2.0
========================================================== */

import { initNavigation } from './navigation.js';
import { initAnimations } from './animations.js';
import { initGallery }    from './gallery.js';
import { initImageFallbacks } from './utilities.js';
import { renderCredentialsRegistry } from './credentials-registry.js';
import { initCredentialsModal } from './credentials-modal.js';
import { initContactReveal } from './contact-reveal.js';

// Module scripts are deferred by default — they run after the HTML
// is parsed, so DOMContentLoaded may already have fired. If the
// document is still loading, wait for it; otherwise initialise now.
function bootstrap() {
    initNavigation();
    initAnimations();
    initGallery();
    renderCredentialsRegistry();
    initImageFallbacks();
    initCredentialsModal();
    initContactReveal();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
} else {
    bootstrap();
}
