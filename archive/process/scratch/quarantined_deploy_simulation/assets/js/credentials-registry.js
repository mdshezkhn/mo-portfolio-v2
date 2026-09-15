/* ==========================================================
   credentials-registry.js
   Museum-Grade Data-Driven Evidence Registry & Renderer
   Part of: Mohammed Shehzad Khan Digital Portfolio v2.0
========================================================== */

export const CREDENTIALS_REGISTRY = [
    // --- EDUCATION SECTION ---
    {
        id: "pgce",
        type: "education",
        title: "Postgraduate Certificate in Education (PGCE)",
        institution: "University of Cumbria, UK",
        period: "2025 — 2026",
        year: 2026,
        featured: true,
        public: true,
        verification: "Verified Qualification",
        verification_details: "Official documentary evidence has been reviewed. Sensitive personal information has been redacted before publication.",
        description: "Primary Education • Master's Level (60 Credits) • Modules PGCE7000 & PGCE7002",
        certificate: "assets/images/certificates/pgce-doc-full.webp",
        thumbnail: "assets/images/certificates/pgce-doc-thumb.webp",
        alt: "Official Certificate Preview: Postgraduate Certificate in Education (PGCE), University of Cumbria",
        has_modal: true,
        availability: "Available upon request",
        // Institution-specific modal layout data
        modal_layout: {
            "Award": "Postgraduate Certificate in Education (non QTS)",
            "Modules": "Raising Achievement • Quality Teaching (Pass)",
            "Credits": "60 (Master's Level)",
            "Classification": "Pass"
        }
    },
    {
        id: "bed",
        type: "education",
        title: "Bachelor of Education (B.Ed.)",
        institution: "University of Kashmir",
        period: "2021 — 2024",
        year: 2024,
        featured: true,
        public: true,
        verification: "Verified Qualification",
        verification_details: "Official documentary evidence has been reviewed. Sensitive personal information has been redacted before publication.",
        description: "Professional Teacher Qualification • Specialization in Pedagogy & Curriculum Design",
        certificate: "assets/images/certificates/bed-doc-full.webp",
        thumbnail: "assets/images/certificates/bed-doc-thumb.webp",
        alt: "Official Degree Preview: Bachelor of Education (B.Ed.), University of Kashmir",
        has_modal: true,
        availability: "Available upon request",
        modal_layout: {
            "Degree": "Bachelor of Education (B.Ed)",
            "University": "University of Kashmir",
            "Year": "2024",
            "Medium of Instruction": "English"
        }
    },
    {
        id: "ma",
        type: "education",
        title: "M.A. in English Language & Literature",
        institution: "Harris University (USA)",
        period: "2007 — 2009",
        year: 2009,
        featured: false,
        public: true,
        verification: "Verified Qualification",
        verification_details: "Official documentary evidence has been reviewed. Sensitive personal information has been redacted before publication.",
        description: "Master of Arts degree in English Language and Literature.",
        certificate: "assets/images/certificates/ma-doc-full.webp",
        thumbnail: "assets/images/certificates/ma-doc-thumb.webp",
        alt: "Document Record: M.A. in English Language & Literature, Harris University",
        has_modal: true,
        availability: "Available upon request",
        modal_layout: {
            "Degree": "Master of Arts",
            "Specialization": "English",
            "University": "Harris University",
            "Year": "2009"
        }
    },
    {
        id: "bsc",
        type: "education",
        title: "Bachelor of Science in Physics (B.Sc.)",
        institution: "University of Mumbai",
        period: "2004 — 2007",
        year: 2007,
        featured: true,
        public: true,
        verification: "Verified Qualification",
        verification_details: "Official documentary evidence has been reviewed. Sensitive personal information has been redacted before publication.",
        description: "Specialization: Physics & Physical Sciences • Foundation in STEM & Scientific Methodology",
        certificate: "assets/images/certificates/bsc-doc-full.webp",
        thumbnail: "assets/images/certificates/bsc-doc-thumb.webp",
        alt: "Official Degree Preview: Bachelor of Science in Physics, University of Mumbai",
        has_modal: true,
        availability: "Available upon request",
        modal_layout: {
            "Degree": "Bachelor of Science",
            "University": "University of Mumbai",
            "Year": "2007",
            "Classification": "Pass Class"
        }
    },

    // --- PROFESSIONAL QUALIFICATIONS & DEVELOPMENT ---
    {
        id: "tesol-collection",
        type: "professional",
        title: "Global TESOL Professional Collection",
        institution: "Global TESOL College, Canada",
        period: "November 2017",
        year: 2017,
        featured: true,
        public: true,
        verification: "Verified Qualification",
        verification_details: "Official documentary evidence has been reviewed. Sensitive personal information has been redacted before publication.",
        description: "Teaching English to Speakers of Other Languages — Advanced pedagogy and business English specialization.",
        thumbnail: "assets/images/certificates/tesol-adv-doc-thumb.webp",
        alt: "Official Certificate Preview: TESOL Certification Collection, Global TESOL College Canada",
        has_modal: true,
        is_collection: true,
        collection_count: 3,
        tags: ["Advanced Pedagogy", "Business English", "Foundations"],
        gallery: [
            "assets/images/certificates/tesol-adv-doc-full.webp",
            "assets/images/certificates/tesol-bus-doc-full.webp",
            "assets/images/certificates/tesol-found-doc-full.webp"
        ],
        availability: "Available upon request",
        modal_layout: {
            "Certificate 1": "Advanced TESOL Certificate (120 Hour)",
            "Certificate 2": "TESOL Specialization: Teaching Business English (60 Hour)",
            "Certificate 3": "Foundation TESOL Certificate (60 Hour)"
        }
    },
    {
        id: "tefl",
        type: "professional",
        title: "TEFL Certification (120 hrs)",
        institution: "Teacher Record",
        period: "July 2025",
        year: 2025,
        featured: true,
        public: true,
        verification: "Verified Qualification",
        verification_details: "Official documentary evidence has been reviewed. Sensitive personal information has been redacted before publication.",
        description: "Teaching English as a Foreign Language across international & multilingual contexts.",
        certificate: "assets/images/certificates/tefl-doc-full.webp",
        thumbnail: "assets/images/certificates/tefl-doc-thumb.webp",
        alt: "Official Certificate Preview: TEFL Certification (120 hrs), Teacher Record",
        has_modal: true,
        availability: "Available upon request",
        modal_layout: {
            "Certificate": "Teaching English as a Foreign Language (120 Hours)",
            "Institution": "TEFL Professional Institute - Teacher Record",
            "Grade": "Distinction",
            "Year": "2025"
        }
    },
    {
        id: "unicef",
        type: "professional",
        title: "What We Stand For: Essentials of Children's Rights",
        institution: "UNICEF",
        period: "April 2026",
        year: 2026,
        featured: true,
        public: true,
        verification: "Verified Qualification",
        verification_details: "Official documentary evidence has been reviewed. Sensitive personal information has been redacted before publication.",
        description: "Professional learning focused on children's rights, safeguarding, child protection, equity, inclusive education, and the UN Convention on the Rights of the Child.",
        certificate: "assets/images/certificates/unicef-doc-full.webp",
        thumbnail: "assets/images/certificates/unicef-doc-thumb.webp",
        alt: "Official Completion Preview: UNICEF Certificate",
        has_modal: true,
        availability: "Available upon request",
        modal_layout: {
            "Course Overview": "Essentials of Children's Rights and child protection frameworks.",
            "Certificate": "Certificate of Completion",
            "Learning Outcomes": "Safeguarding, equity, inclusive education, UN Convention on the Rights of the Child"
        }
    }
];

export function renderCredentialsRegistry() {
    const eduContainer = document.getElementById('edu-grid-container');
    const profContainer = document.getElementById('prof-grid-container');

    if (!eduContainer && !profContainer) return;

    const eduItems = CREDENTIALS_REGISTRY.filter(item => item.type === 'education' && item.public);
    const profItems = CREDENTIALS_REGISTRY.filter(item => item.type === 'professional' && item.public);

    function createCardHTML(item) {
        const isDocumented = item.is_documented;
        const badgeClass = isDocumented ? 'v-badge v-badge--documented' : 'v-badge';
        const badgeIcon = isDocumented ? 'ℹ' : '✓';
        const overlayText = isDocumented ? '🔍 View archive record' : (item.is_collection ? '🔍 View collection' : '🔍 Click to enlarge');

        const tagsHTML = item.tags ? `
            <div class="cert-tags">
                ${item.tags.map(tag => `<span class="cert-tag">${tag}</span>`).join('')}
            </div>
        ` : '';

        // Safely stringify the modal layout and gallery for the DOM
        const modalLayoutJSON = encodeURIComponent(JSON.stringify(item.modal_layout || {}));
        const galleryJSON = encodeURIComponent(JSON.stringify(item.gallery || (item.certificate ? [item.certificate] : [])));

        const badgeHTML = item.hide_badge ? '' : `<span class="${badgeClass}">${badgeIcon} ${item.verification}</span>`;

        return `
            <div class="${item.type === 'education' ? 'edu-card' : 'cert-card'}" 
                 data-cert-id="${item.id}"
                 data-title="${item.title}" 
                 data-issuer="${item.institution}" 
                 data-status="${item.verification}" 
                 data-gallery="${galleryJSON}"
                 data-layout="${modalLayoutJSON}">
                <div class="cert-thumb">
                    <picture>
                        <source srcset="${item.thumbnail}" type="image/webp">
                        <img src="${item.thumbnail}" alt="${item.alt}" loading="lazy" width="400" height="280">
                    </picture>
                    ${item.is_collection ? `<span class="collection-badge">${item.collection_count} Verified Certificates</span>` : ''}
                    <span class="cert-thumb-overlay">${overlayText}</span>
                </div>
                <h4 class="${item.type === 'education' ? 'edu-deg' : 'cert-title'}">${item.title}</h4>
                <p class="${item.type === 'education' ? 'edu-sch' : 'cert-issuer'}">${item.institution}</p>
                <time class="${item.type === 'education' ? 'edu-yr' : 'cert-period'}">${item.period}</time>
                <p class="cert-desc">${item.description}</p>
                ${tagsHTML}
                <div class="verification-panel">
                    ${badgeHTML}
                    <div class="v-details">${item.verification_details}</div>
                </div>
            </div>
        `;
    }

    if (eduContainer) {
        eduContainer.innerHTML = eduItems.map(createCardHTML).join('');
    }

    if (profContainer) {
        profContainer.innerHTML = profItems.map(createCardHTML).join('');
    }
}
