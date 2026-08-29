/* ==========================================================
   credentials-modal.js
   Museum-Grade Lightbox Modal, Interactive Zoom & Evidence Standards Handler
   Part of: Mohammed Shehzad Khan Digital Portfolio v2.0
========================================================== */

export function initCredentialsModal() {
    const cards = Array.from(document.querySelectorAll('.cert-card, .edu-card')).filter(c => c.hasAttribute('data-cert-id'));
    const modal = document.getElementById('credential-modal');
    if (!modal) return;

    const modalImg = modal.querySelector('.modal-img');
    const modalTitle = modal.querySelector('.modal-title');
    const modalIssuer = modal.querySelector('.modal-issuer');
    const modalStatus = modal.querySelector('.modal-status-badge');
    const modalYear = modal.querySelector('.modal-exhibit-year');
    const modalSupportingList = modal.querySelector('.modal-supporting-list');
    const closeBtn = modal.querySelector('.modal-close');
    const prevBtn = modal.querySelector('.modal-prev');
    const nextBtn = modal.querySelector('.modal-next');
    const zoomInBtn = modal.querySelector('.zoom-in');
    const zoomOutBtn = modal.querySelector('.zoom-out');
    const zoomResetBtn = modal.querySelector('.zoom-reset');
    const modalTabsContainer = modal.querySelector('.modal-tabs');
    const certTabBtn = modal.querySelector('.tab-cert');
    const transcriptTabBtn = modal.querySelector('.tab-transcript');

    // Evidence Standards Modal elements
    const standardsModal = document.getElementById('evidence-standards-modal');
    const standardsOpenBtns = document.querySelectorAll('.trigger-evidence-standards');
    const standardsCloseBtn = standardsModal ? standardsModal.querySelector('.standards-close') : null;

    let currentIndex = 0;
    let previousActiveElement = null;
    let currentZoomScale = 1.0;
    
    // For handling galleries
    let currentGallery = [];
    let currentGalleryIndex = 0;

    function setZoom(scale) {
        currentZoomScale = Math.min(Math.max(scale, 0.8), 2.5);
        if (modalImg) {
            modalImg.style.transform = `scale(${currentZoomScale})`;
            if (currentZoomScale > 1.0) {
                modalImg.classList.add('is-zoomed');
            } else {
                modalImg.classList.remove('is-zoomed');
            }
        }
    }

    function resetZoom() {
        setZoom(1.0);
    }

    function updateGalleryImage() {
        if (!currentGallery || currentGallery.length === 0) return;
        resetZoom();
        if (modalImg) {
            modalImg.src = currentGallery[currentGalleryIndex];
            modalImg.alt = `Official Award Certificate: ${modalTitle ? modalTitle.textContent : 'Credential'}`;
        }
        
        // Update tabs if it's a gallery
        if (modalTabsContainer && currentGallery.length > 1) {
            modalTabsContainer.style.display = 'flex';
            modalTabsContainer.innerHTML = currentGallery.map((_, i) => 
                `<button type="button" class="modal-tab-btn ${i === currentGalleryIndex ? 'is-active' : ''}" data-index="${i}">
                    Document ${i + 1}
                </button>`
            ).join('');
            
            // Rebind tab clicks
            const tabs = modalTabsContainer.querySelectorAll('.modal-tab-btn');
            tabs.forEach(tab => {
                tab.addEventListener('click', (e) => {
                    currentGalleryIndex = parseInt(e.target.getAttribute('data-index'), 10);
                    updateGalleryImage();
                });
            });
        } else if (modalTabsContainer) {
            modalTabsContainer.style.display = 'none';
        }
    }

    function openModal(index) {
        currentIndex = index;
        const card = cards[currentIndex];
        if (!card) return;

        previousActiveElement = document.activeElement;

        const title = card.getAttribute('data-title') || '';
        const issuer = card.getAttribute('data-issuer') || '';
        const year = card.getAttribute('data-year') || '';
        // Status defaults to a neutral credential label. The earlier
        // "Verified Qualification" wording exposed the internal
        // provenance/verification machinery to visitors; the badge
        // now communicates the credential itself rather than how it
        // was verified.
        const status = card.getAttribute('data-status') || 'Awarded';
        
        let layoutData = {};
        try {
            layoutData = JSON.parse(decodeURIComponent(card.getAttribute('data-layout') || '%7B%7D'));
        } catch (e) {
            layoutData = {};
        }

        try {
            currentGallery = JSON.parse(decodeURIComponent(card.getAttribute('data-gallery') || '%5B%5D'));
        } catch(e) {
            currentGallery = [];
        }
        
        currentGalleryIndex = 0;

        if (modalTitle) modalTitle.textContent = title;
        if (modalIssuer) modalIssuer.textContent = issuer;
        if (modalYear) modalYear.textContent = year ? `Awarded: ${year}` : '';

        if (modalStatus) {
            modalStatus.textContent = status.toLowerCase().includes('documented') ? `ℹ ${status}` : `✓ ${status}`;
            if (status.toLowerCase().includes('documented')) {
                modalStatus.classList.add('documented');
            } else {
                modalStatus.classList.remove('documented');
            }
        }

        if (modalSupportingList) {
            const layoutHtml = Object.entries(layoutData).map(([key, val]) => 
                `<li style="margin-bottom: 0.5rem;"><strong style="color: var(--text-primary); display:block; font-size:0.85rem;">${key}</strong><span style="font-size: 0.95rem;">${val}</span></li>`
            ).join('');
            
            modalSupportingList.innerHTML = layoutHtml;
        }

        updateGalleryImage();

        modal.classList.add('is-active');
        modal.setAttribute('aria-hidden', 'false');
        modal.hidden = false;
        document.body.style.overflow = 'hidden';

        if (closeBtn) closeBtn.focus();
    }

    function closeModal() {
        modal.classList.remove('is-active');
        modal.setAttribute('aria-hidden', 'true');
        modal.hidden = true;
        document.body.style.overflow = '';
        resetZoom();

        if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
            previousActiveElement.focus();
        }
    }

    function showPrev() {
        if (cards.length === 0) return;
        const newIndex = (currentIndex - 1 + cards.length) % cards.length;
        openModal(newIndex);
    }

    function showNext() {
        if (cards.length === 0) return;
        const newIndex = (currentIndex + 1) % cards.length;
        openModal(newIndex);
    }

    // Evidence Standards Modal Functions
    function openStandardsModal() {
        if (!standardsModal) return;
        previousActiveElement = document.activeElement;
        standardsModal.classList.add('is-active');
        standardsModal.setAttribute('aria-hidden', 'false');
        standardsModal.hidden = false;
        document.body.style.overflow = 'hidden';
        if (standardsCloseBtn) standardsCloseBtn.focus();
    }

    function closeStandardsModal() {
        if (!standardsModal) return;
        standardsModal.classList.remove('is-active');
        standardsModal.setAttribute('aria-hidden', 'true');
        standardsModal.hidden = true;
        document.body.style.overflow = '';
        if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
            previousActiveElement.focus();
        }
    }

    cards.forEach((card, idx) => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `View documentary evidence exhibit for ${card.getAttribute('data-title') || 'Qualification'}`);

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

    if (zoomInBtn) zoomInBtn.addEventListener('click', () => setZoom(currentZoomScale + 0.3));
    if (zoomOutBtn) zoomOutBtn.addEventListener('click', () => setZoom(currentZoomScale - 0.3));
    if (zoomResetBtn) zoomResetBtn.addEventListener('click', resetZoom);

    if (modalImg) {
        modalImg.addEventListener('click', () => {
            if (currentZoomScale > 1.0) {
                resetZoom();
            } else {
                setZoom(1.5);
            }
        });
    }

    modal.addEventListener('click', (e) => {
        if (e.target === modal || e.target.classList.contains('credential-modal')) {
            closeModal();
        }
    });

    // Evidence Standards Event Handlers
    standardsOpenBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            openStandardsModal();
        });
    });

    if (standardsCloseBtn) standardsCloseBtn.addEventListener('click', closeStandardsModal);
    if (standardsModal) {
        standardsModal.addEventListener('click', (e) => {
            if (e.target === standardsModal || e.target.classList.contains('standards-backdrop')) {
                closeStandardsModal();
            }
        });
    }

    // Keyboard Focus Trap & Shortcuts
    document.addEventListener('keydown', (e) => {
        const activeModal = standardsModal && standardsModal.classList.contains('is-active') ? standardsModal : (modal.classList.contains('is-active') ? modal : null);
        if (!activeModal) return;

        if (e.key === 'Escape') {
            if (standardsModal && standardsModal.classList.contains('is-active')) {
                closeStandardsModal();
            } else {
                closeModal();
            }
        } else if (e.key === 'ArrowLeft' && activeModal === modal) {
            showPrev();
        } else if (e.key === 'ArrowRight' && activeModal === modal) {
            showNext();
        } else if (e.key === 'Tab') {
            const focusableElements = Array.from(
                activeModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
            );
            if (focusableElements.length === 0) return;

            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        }
    });
}
