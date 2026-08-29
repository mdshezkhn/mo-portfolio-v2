/* ==========================================================
   contact-reveal.js
   Toggles the contact-section reveal-on-click channels
   (WeChat, WhatsApp, Email, LinkedIn). Each row's phone number,
   email address, profile link, and QR thumbnail stays hidden
   until the user explicitly expands the row. The label stays
   visible so the visitor knows what channels are available.
   Part of: Mohammed Shehzad Khan Portfolio v2.0
========================================================== */

export function initContactReveal() {
    const toggles = document.querySelectorAll('.contact-toggle');
    if (!toggles.length) return;

    toggles.forEach(function (button) {
        button.addEventListener('click', function () {
            const expanded = button.getAttribute('aria-expanded') === 'true';
            const targetId = button.getAttribute('aria-controls');
            if (!targetId) return;
            const panel = document.getElementById(targetId);
            if (!panel) return;

            // Toggle this channel
            const nextExpanded = !expanded;
            button.setAttribute('aria-expanded', String(nextExpanded));
            if (nextExpanded) {
                panel.removeAttribute('hidden');
            } else {
                panel.setAttribute('hidden', '');
            }
        });
    });
}
