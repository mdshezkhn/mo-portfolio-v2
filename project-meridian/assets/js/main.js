/**
 * Project Meridian - main.js
 * Core JavaScript functionality including Scroll Reveal via IntersectionObserver.
 */

document.addEventListener('DOMContentLoaded', () => {
    initScrollReveal();
    initHeaderScroll();
});

/**
 * Initializes the header scroll state.
 * Adds the 'is-scrolled' class when the user scrolls down.
 */
function initHeaderScroll() {
    const header = document.querySelector('.site-header');
    if (!header) return;

    const handleScroll = () => {
        if (window.scrollY > 50) {
            header.classList.add('is-scrolled');
        } else {
            header.classList.remove('is-scrolled');
        }
    };

    // Initial check
    handleScroll();

    // Listen for scroll
    window.addEventListener('scroll', handleScroll, { passive: true });
}

/**
 * Initializes the scroll reveal animations using IntersectionObserver.
 * Elements with the [data-reveal] attribute will fade in when they enter the viewport.
 */
function initScrollReveal() {
    // Respect user preference for reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    const revealElements = document.querySelectorAll('[data-reveal]');
    
    if (!revealElements.length) return;

    const revealOptions = {
        root: null,
        rootMargin: '0px 0px -10% 0px', // Triggers slightly before element comes fully into view
        threshold: 0.1
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add the class that triggers the CSS transition
                entry.target.classList.add('is-revealed');
                
                // Stop observing the element once it has been revealed
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
}
