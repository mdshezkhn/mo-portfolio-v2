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

document.addEventListener('DOMContentLoaded', function () {
    initNavigation();
    initAnimations();
    initGallery();
    renderCredentialsRegistry();
    initImageFallbacks();
    initCredentialsModal();
});
