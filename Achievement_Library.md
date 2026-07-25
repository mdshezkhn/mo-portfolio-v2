# Achievement Library (VAL)

**Role:** the canonical source of achievements. Every public output — Career Timeline, Portfolio,
CV, LinkedIn, Interview Prep, Cover Letters — is generated from this file. Store *canonical data*
here (core fact, context, impact, evidence, hiring value); generate the channel views (CV bullet,
LinkedIn line, interview answer, portfolio paragraph) on demand from these fields. Do not store
generated views — that creates parallel copies to maintain forever.

**Pipeline**
```
Evidence Source → Evidence Register → Achievement Library → Career Timeline → Portfolio / CV / LinkedIn / Interview Prep / Cover Letters
```
The Career Timeline is a *generated* chronology that organises these achievements by date; it is
not the source. Never hand-edit a downstream artifact — update the canonical field here, regenerate.

**Status:** v0.1 Seed. Entries are derived from the canonical career timeline and the live
portfolio. No primary evidence document has been processed yet, so every entry is
**Evidence Strength: Single Source** (the timeline only) and **Verification Status: Pending**.

**Evidence Strength** (how strong the backing evidence is)
- **Primary** — a primary document exists (employment letter, certificate).
- **Multiple Sources** — corroborated by two or more independent sources (timeline + CV + manager email).
- **Single Source** — backed by only one source (the canonical timeline, before a primary document is processed).

**Verification Status** (lifecycle state): `Pending → Verified → Superseded / Archived`.

**Schema (per entry)**
`ID | Hiring Value | Evidence Type | Evidence Strength | Verification Status | Core Fact | Context | Impact | Evidence | Interview Topic`

---

## VA-001 — Led instructional quality for a distributed teaching team
- **Hiring Value:** Leadership · Instructional Quality
- **Evidence Type:** Employment
- **Evidence Strength:** Single Source *(canonical timeline; primary employment letter pending)*
- **Verification Status:** Pending
- **Core Fact:** Led instructional quality and educator-development initiatives for a distributed teaching team.
- **Context:** Remote, high-scale EdTech environment (WhiteHat Jr / BYJU'S), 2020–2022.
- **Impact:** Improved instructional consistency and coaching standards across the team. *(Cohort size is PENDING VERIFICATION — 200 vs 1,000 educators. Do not publish a specific figure until the employment letter is processed; the canonical timeline holds `SCOPE PENDING (200 vs 1,000)`.)*
- **Evidence:** Employment letter (Pending).
- **Interview Topic:** Instructional Leadership

## VA-002 — Led training & QA for trainers across three markets
- **Hiring Value:** Leadership · Training
- **Evidence Type:** Employment
- **Evidence Strength:** Single Source
- **Verification Status:** Pending
- **Core Fact:** Led training and quality-assurance programmes for a team of 15+ trainers.
- **Context:** Multi-campus organisation across UK, Dubai and Malta, 2022–2023.
- **Impact:** Standardised training and QA across three markets; raised trainer capability and consistency.
- **Evidence:** Employment letter (Pending).
- **Interview Topic:** Training & Quality

## VA-003 — Mentored new teachers & led writing moderation
- **Hiring Value:** Mentoring · Assessment
- **Evidence Type:** Employment
- **Evidence Strength:** Single Source
- **Verification Status:** Pending
- **Core Fact:** Mentored newly appointed teachers and led Grade 5 writing moderation.
- **Context:** Aoxin International School, primary team, 2018–2020.
- **Impact:** Built instructional consistency across the primary team; accelerated new-teacher ramp-up.
- **Evidence:** Employment letter (Pending).
- **Interview Topic:** Mentoring & Assessment

## VA-004 — Early-years teacher training & modelling
- **Hiring Value:** Training · Early Years
- **Evidence Type:** Employment
- **Evidence Strength:** Single Source
- **Verification Status:** Pending
- **Core Fact:** Delivered early-years ESL instruction and modelled practice while training kindergarten educators.
- **Context:** Eton House Kindergarten, China, 2017–2018.
- **Impact:** Strengthened kindergarten teaching practice through modelling and demonstration lessons.
- **Evidence:** Employment letter (Pending).
- **Interview Topic:** Early-Years Practice

## VA-005 — Built spoken-confidence ESL programmes
- **Hiring Value:** EAL / ESL · Curriculum
- **Evidence Type:** Employment
- **Evidence Strength:** Single Source
- **Verification Status:** Pending
- **Core Fact:** Built spoken-confidence and communicative ESL programmes for secondary learners.
- **Context:** Zhejiang University / Helen China TEFL Network, middle & high school, 2016–2017.
- **Impact:** Raised oral participation and fluency among secondary ESL learners.
- **Evidence:** Employment letter (Pending).
- **Interview Topic:** EAL / ESL Practice

---

## How to extend
1. New core fact verified → add an Evidence Register entry → add a VAL entry here (set Evidence Strength + Verification Status) → regenerate downstream.
2. Presentation-only changes (hero wording, section order, layout, microcopy) do **not** get a VAL entry.
3. When a primary document arrives: raise Evidence Strength (Single Source → Multiple Sources → Primary) and flip Verification Status to Verified, then regenerate every view from the canonical fields.
4. *Future evolution (not built yet):* one achievement can generate many recruiter **claims** (e.g. "mentored Grade 5 teachers" → "experienced mentor", "improves assessment consistency", "can lead moderation"). A Claim Library could sit between the Achievement Library and public outputs. Deferred — execution matters more than architecture for now.
