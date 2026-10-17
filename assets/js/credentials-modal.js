/* ==========================================================
   credentials-modal.js
   Accessible Lightbox Modal & Evidence Verification Panel Handler
   Part of: Mohammed Shehzad Khan Portfolio v2.0
========================================================== */

export function initCredentialsModal() {
    const cards = Array.from(document.querySelectorAll('.cert-card[data-cert-src], .edu-card[data-cert-src]'));
    const modal = document.getElementById('credential-modal');
    if (!modal || cards.length === 0) return;

    const modalImg = modal.querySelector('.modal-img');
    const modalTitle = modal.querySelector('.modal-title');
    const modalIssuer = modal.querySelector('.modal-issuer');
    const modalStatus = modal.querySelector('.modal-status-badge');
    const modalEvidence = modal.querySelector('.modal-evidence-id');
    const modalNotes = modal.querySelector('.modal-notes');
    const closeBtn = modal.querySelector('.modal-close');
    const prevBtn = modal.querySelector('.modal-prev');
    const nextBtn = modal.querySelector('.modal-next');

    let currentIndex = 0;
    let previousActiveElement = null;

    function openModal(index) {
        currentIndex = index;
        const card = cards[currentIndex];
        if (!card) return;

        previousActiveElement = document.activeElement;

        const src = card.getAttribute('data-cert-src');
        const title = card.getAttribute('data-title') || '';
        const issuer = card.getAttribute('data-issuer') || '';
        const status = card.getAttribute('data-status') || 'Verified Evidence';
        const evidenceId = card.getAttribute('data-evidence-id') || '';
        const notes = card.getAttribute('data-notes') || 'Sensitive registration numbers redacted for privacy.';

        if (modalImg) {
            modalImg.src = src;
            modalImg.alt = `Official Certificate Evidence Preview: ${title}`;
        }
        if (modalTitle) modalTitle.textContent = title;
        if (modalIssuer) modalIssuer.textContent = issuer;
        if (modalStatus) modalStatus.textContent = `✓ ${status}`;
        if (modalEvidence) modalEvidence.textContent = evidenceId ? `Evidence ID: ${evidenceId}` : '';
        if (modalNotes) modalNotes.textContent = notes;

        modal.classList.add('is-active');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';

        if (closeBtn) closeBtn.focus();
    }

    function closeModal() {
        modal.classList.remove('is-active');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';

        if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
            previousActiveElement.focus();
        }
    }

    function showPrev() {
        const newIndex = (currentIndex - 1 + cards.length) % cards.length;
        openModal(newIndex);
    }

    function showNext() {
        const newIndex = (currentIndex + 1) % cards.length;
        openModal(newIndex);
    }

    cards.forEach((card, idx) => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `View evidence for ${card.getAttribute('data-title') || 'Qualification'}`);

        card.addEventListener('click', () => openModal(idx));
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openModal(idx);
            }
        });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (prevBtn) prevBtn.addEventListener('click', showPrev);
    if (nextBtn) nextBtn.addEventListener('click', showNext);

    modal.addEventListener('click', (e) => {
        if (e.target === modal || e.target.classList.contains('modal-backdrop')) {
            closeModal();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (!modal.classList.contains('is-active')) return;

        if (e.key === 'Escape') {
            closeModal();
        } else if (e.key === 'ArrowLeft') {
            showPrev();
        } else if (e.key === 'ArrowRight') {
            showNext();
        }
    });
}
