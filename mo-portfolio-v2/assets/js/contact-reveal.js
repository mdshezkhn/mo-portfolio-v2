/* ==========================================================
   contact-reveal.js
   Contact-section modal launcher. Clicking a contact-link
   (WeChat, WhatsApp, Email, LinkedIn) opens a single shared
   modal whose body is populated from a channel-specific
   template. Phone numbers, email addresses, profile URLs, and
   QR thumbnails stay hidden until the visitor explicitly
   opens the channel they want.
   Part of: Mohammed Shehzad Khan Portfolio v2.0
========================================================== */

const CHANNEL_CONTENT = {
    wechat: {
        title: 'Connect on WeChat',
        subtitle: 'China — main mobile, also reachable on WeChat',
        bodyHtml: `
            <div class="contact-modal-channel">
                <p class="contact-modal-label">WeChat ID / Mobile</p>
                <p class="contact-modal-value">+86-131 3771 9002</p>
                <p class="contact-modal-hint">Scan the QR code below with the WeChat app to add me as a contact, or send the number above.</p>
                <div class="contact-modal-qr-wrap">
                    <img src="assets/images/social/wechat-qr.png" alt="WeChat QR code" class="contact-modal-qr" loading="lazy">
                </div>
            </div>
        `
    },
    whatsapp: {
        title: 'Connect on WhatsApp',
        subtitle: 'India — also reachable on WhatsApp',
        bodyHtml: `
            <div class="contact-modal-channel">
                <p class="contact-modal-label">WhatsApp / Mobile</p>
                <p class="contact-modal-value">+91 98695 06845</p>
                <p class="contact-modal-hint">Scan the QR code below with the WhatsApp app, or send the number above.</p>
                <div class="contact-modal-qr-wrap">
                    <img src="assets/images/social/whatsapp-qr.png" alt="WhatsApp QR code" class="contact-modal-qr" loading="lazy">
                </div>
            </div>
        `
    },
    email: {
        title: 'Send an email',
        subtitle: 'Opens your default mail client',
        bodyHtml: `
            <div class="contact-modal-channel">
                <p class="contact-modal-label">Email address</p>
                <p class="contact-modal-value">mdshezkhn@hotmail.com</p>
                <p class="contact-modal-hint">Click the button below to open your mail client with this address pre-filled. If nothing happens, copy the address and send it manually.</p>
                <div class="contact-modal-actions">
                    <a href="mailto:mdshezkhn@hotmail.com" class="btn btn-primary">Open mail client</a>
                </div>
            </div>
        `
    },
    linkedin: {
        title: 'Connect on LinkedIn',
        subtitle: 'Opens profile in a new tab',
        bodyHtml: `
            <div class="contact-modal-channel">
                <p class="contact-modal-label">LinkedIn profile</p>
                <p class="contact-modal-value">linkedin.com/in/mdshezkhn</p>
                <p class="contact-modal-hint">Click the button below to open my LinkedIn profile in a new tab.</p>
                <div class="contact-modal-actions">
                    <a href="https://www.linkedin.com/in/mdshezkhn" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Open LinkedIn profile</a>
                </div>
            </div>
        `
    }
};

export function initContactReveal() {
    const triggers = document.querySelectorAll('.contact-open-modal');
    const modal = document.getElementById('contact-modal');
    if (!triggers.length || !modal) return;

    const titleEl = modal.querySelector('#contact-modal-title');
    const subtitleEl = modal.querySelector('#contact-modal-subtitle');
    const bodyEl = modal.querySelector('.contact-modal-body');
    const closeBtn = modal.querySelector('.contact-modal-close');

    let previousActiveElement = null;

    function openModal(channelKey) {
        const channel = CHANNEL_CONTENT[channelKey];
        if (!channel) return;

        previousActiveElement = document.activeElement;

        titleEl.textContent = channel.title;
        subtitleEl.textContent = channel.subtitle;
        bodyEl.innerHTML = channel.bodyHtml;

        modal.classList.add('is-active');
        modal.setAttribute('aria-hidden', 'false');
        modal.hidden = false;
        document.body.style.overflow = 'hidden';

        if (closeBtn) closeBtn.focus({ preventScroll: true });
    }

    function closeModal() {
        modal.classList.remove('is-active');
        modal.setAttribute('aria-hidden', 'true');
        modal.hidden = true;
        document.body.style.overflow = '';
        bodyEl.innerHTML = '';

        if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
            previousActiveElement.focus({ preventScroll: true });
        }
    }

    triggers.forEach(function (trigger) {
        trigger.addEventListener('click', function () {
            const channelKey = trigger.getAttribute('data-contact-channel');
            openModal(channelKey);
        });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeModal);

    // Backdrop click closes the modal
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Escape key closes the modal
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-active')) {
            closeModal();
        }
    });
}
