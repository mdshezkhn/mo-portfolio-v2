# Evidence Acquisition Plan

> **Evidence Pipeline — Version 1.0 · Status: Frozen**
> Baseline is fixed. Architecture changes permitted only if: execution exposes a throughput defect ·
> verification quality decreases · recruiter trust is negatively affected. Any future change is
> justified against v1.0, not made ad hoc.

> **Frozen scope (v1.0) — not changing without a defect:**
> Source-of-truth hierarchy · Verification model · Evidence acquisition workflow · Regeneration SOP ·
> Provenance model · Operational metrics · Phase exit criteria · Reporting template (editable within
> this plan, but not a reason to revisit architecture). Anything outside this list must satisfy the
> governing rule; if it doesn't improve throughput, verification quality, or recruiter trust, it goes
> to the v2 backlog.

> **Governing rule — decision filter for every proposed change:**
> If a proposed change does not increase **evidence throughput**, **verification quality**, or
> **recruiter trust**, defer it until v2.
>
> Someone suggests redesigning the Achievement Library? Does it improve throughput? No → deferred.
> Changing typography? Recruiter trust? Probably not → deferred. A parser that cuts verification time
> from 30 min to 5? Throughput? Yes → do it. This rule stops the project drifting back into
> architecture work disguised as progress.

**Purpose:** the prioritized production backlog. Each row is a piece of evidence to acquire,
ranked by hiring impact. Acquiring an item moves its Evidence Register entry from `Pending` to
`Verified`, which lets the canonical timeline and Achievement Library regenerate with confirmed
figures. This is the active work queue — a production asset, not a governance doc.

**How it feeds the pipeline**
```
Acquire evidence → Evidence Register (Pending → Verified) → Canonical Timeline → Achievement Library
                → regenerate Portfolio / CV / LinkedIn / Interview Prep / Cover Letters
```

## Priority table

| Priority | Evidence | Hiring Impact | Unblocks | Status |
|----------|----------|---------------|----------|--------|
| **P0** | Employment letters (all 7 roles) | Critical — primary evidence; verifies roles, dates, scope; resolves the 200 vs 1,000 open question | Canonical Timeline, VAL confidence | Not started |
| **P0** | PGCE certificate / exam-board ratification | Critical — validates the centerpiece qualification | Credentials section, VAL research entry | Not started |
| **P1** | Current CV (PDF) | High — *derived* artifact; regenerate from verified employment + PGCE, do NOT write ahead of primary evidence | Portfolio CV link, LinkedIn, VAL variants | Not started |
| **P1** | Principal / line-manager testimonial | Very High — third-party credibility | VAL, Interview Prep, Cover Letters | Not started |
| **P1** | Parent communication example | High — answers the "difficult parents?" objection | Portfolio, Interview Prep | Not started |
| **P1** | Lesson observation / walkthrough note | High — answers "confident in front of parents?" | Portfolio, VAL | Not started |
| **P2** | Qualification certificates (B.Ed, MA, TESOL, TEFL, British Council) | Medium-High — verifies credentials | Credentials section | Not started |
| **P2** | Anonymised student work | Medium — shows impact on learning | Portfolio (Classroom), VAL | Not started |
| **P2** | Classroom demonstration video (China-safe host) | Medium — shows practice | Portfolio (Classroom) | Not started |
| **P2** | Contactable professional references | Medium — backs testimonials | Cover Letters, Interview Prep | Not started |

## Acquisition workflows (two distinct pipelines)

Employment verification splits into **HR** and **manager** tracks because they have different
recipients and different success criteria. Run them in parallel.

**HR workflow** — recipient: HR / Records department. Success = a signed letter on company
letterhead confirming administrative facts.
- Employment dates (start – end)
- Job title(s) held
- Employment status (full-time / part-time / contract)
- Department / team
- Letter on company letterhead, signed, as PDF

**Manager workflow** — recipient: former line manager. Success = a confirmation of scope and
impact (and, optionally, a testimonial).
- Responsibilities
- Team scope
- Achievements
- Operational metrics (e.g. educator cohort size)
- Testimonial (optional)

> The `200 vs 1,000` educator-scope question belongs in the **manager** workflow, not HR — large
> HR departments typically will not certify operational metrics. Route it to the line manager.

**Question → best evidence source**

| Question            | Best evidence source |
| ------------------- | -------------------- |
| Employment dates    | HR                   |
| Job title           | HR                   |
| Employment status   | HR                   |
| Responsibilities    | Manager              |
| Team size / scope   | Manager              |
| Performance         | Manager              |
| Leadership examples | Manager              |
| Awards              | Internal documents   |
| Student impact      | Portfolio evidence   |

Different sources answer different questions — route each request to the right workflow above.

## Sequencing
1. Clear **P0** first — employment letters and PGCE cert. These are *primary* evidence; every
   downstream fact (dates, titles, scope) depends on them. The portfolio cannot be frozen for
   review without them — these are the real *hiring* blockers.
2. The **Current CV is regenerated from that verified evidence**, not written ahead of it. Drafting
   the CV before employment letters land means a later date/title/scope correction edits a downstream
   artifact before its upstream — the anti-pattern this pipeline exists to prevent. Fix the CV link
   only once it can be regenerated from P0.
3. Then **P1** — testimonials and observations convert "claims" into "credibility."
4. Then **P2** — classroom artefacts and references add depth.

## Definition of done (per item)
- Document dropped in `/private` (or the asset supplied at its referenced path).
- Evidence Register entry flips `Pending → Verified`.
- Canonical timeline row flips to `Verification Status: Verified`.
- Achievement Library entry raised `Draft → Supported / Verified` and regenerated downstream.

## Current hiring blockers (not release tasks)
- **Missing employment letters** — primary evidence; roles, dates and scope unverified (200 vs 1,000 still open). Everything downstream waits on this.
- **Missing PGCE certificate / ratification** — validates the centerpiece qualification.

> **CV link must never be a broken 404.** The CV is a *derived* artifact and must be regenerated
> from verified employment + PGCE, not written ahead of them — so there is *no downloadable CV until
> verification is complete*. But a recruiter experiences "Click Download CV → 404" as negligence
> regardless of the reasoning. Therefore: show an **intentional placeholder** ("CV temporarily
> unavailable while professional records are being consolidated. A verified version will be published
> once document verification is complete.") or remove the button entirely. A missing resource reads as
> neglect; an intentional placeholder reads as an active update. **Never expose a dead link.**

> **Release task (not a hiring blocker):** the canonical / OG / sitemap / robots URLs still point
> to `…/mo-portfolio-v2/`. A recruiter can still evaluate the site, so this is a pre-launch
> cleanup, not a blocker. Fix the base URL in those spots right before deploy.

## Success metrics (how to judge progress)
- **Primary KPI — Verification coverage: `verified / total`.** Until the Evidence Register has been
  enumerated, report it exactly as: `Verified: 0 · Total tracked claims: TBD · Coverage: TBD`.
  **Do not invent the denominator** — a plausible-looking number (e.g. "42") is worse than TBD,
  because it pretends the ER is complete when it isn't. Once the ER is enumerated, the total becomes
  stable and coverage is reported as a percentage. This answers "how far through the verification
  programme are we?" — distinct from "what happened this week?" Track both. A single employment
  letter can verify ten claims; five screenshots may verify none.
- **Secondary KPI — New evidence sources acquired.** Primary documents entered `/private` and
  processed (employment letter, certificate, testimonial, observation, CV).
- **Operational metric — Evidence Acquisition Lead Time.** Request sent → Evidence received. Measures
  the *external* dependency (how long employers / cert bodies take to respond). Mostly outside
  Claude's control; track it so a slow responder never masquerades as a pipeline problem.
- **Operational metric — Evidence Processing Lead Time.** Evidence received → Claim verified. Measures
  *pipeline efficiency* (how fast a document propagates into verified claims). If this grows, the
  pipeline itself is the constraint — fix propagation, not collection. Example: received 21 Jul →
  ER 21 Jul → VAL 21 Jul → Verified 22 Jul = **1 day**.
- **Avoid as progress signals:** files edited, documents created, lines changed. Those are *activity*,
  not advancement. If the weekly answer to "what new evidence entered?" is "nothing," then nothing
  meaningful happened — however busy the session looked.

## Regeneration SOP (explicit, not implied)

Updating upstream evidence must propagate downstream. Run this checklist every time the Evidence
Register changes — explicit process fails less often than memory. Do not skip steps.

**Trigger:** any change to the Evidence Register (new document, corrected fact, status flip).

- [ ] **Update ER** — add/modify the entry; assign or confirm its Evidence ID; set Status + Last Verified.
- [ ] **Regenerate AL** — reflect the change in `Achievement_Library.md` (canonical fields only; never hand-edit generated views).
- [ ] **Regenerate Timeline** — `career-timeline.md` is generated; never hand-edit it.
- [ ] **Regenerate Portfolio** — `portfolio-v3/index.html` (and `cv-status.html` if CV-affecting).
- [ ] **Regenerate CV** — only once P0 evidence verifies (see Sequencing); never write ahead of upstream.
- [ ] **Regenerate LinkedIn** — consistency check only; LinkedIn is never a source.
- [ ] **Commit** — version-control the changed files.
- [ ] **Verify** — confirm every public claim still traces to its Evidence ID; confirm no stale figure remains.

## Verification model (partial verification)

Verification Status has only two meaningful live states for an entry: **Pending** and **Verified**
(`Superseded` / `Archived` are terminal). Reality is often incremental, so the rule is:

- **Verification Status stays `Pending` until every required canonical field of the entry is verified.**
- **Individual fields may independently reference verified evidence** before the entry as a whole
  flips to `Verified`. Progress is tracked per-field, not per-entry.
- This allows incremental verification (e.g. dates and title verified, team size still open) without
  adding a third status field that would complicate the model.
- Once the last required field is evidenced, flip the entry `Pending → Verified` and record `Last Verified`.

## Phase exit criteria (definition of done)

Framework work for this phase stops when ALL of the following hold. Architecture changes after this
point require a *documented defect that blocks evidence throughput* — not a preference for elegance.

- [ ] Evidence pipeline is stable (ER → AL → outputs, with the Regeneration SOP).
- [ ] Regeneration SOP is documented and runnable by anyone.
- [ ] P0 evidence has been processed (employment letters + PGCE cert).
- [ ] Public portfolio contains **no unverified factual claims** (every public statement traces to a
      verified Evidence ID).
- [ ] No architectural changes unless a defect blocks evidence throughput.

Until these are met, the work is operational: acquire evidence, verify claims, regenerate outputs, repeat.

## First-evidence retrospective

When the first employment letter is processed, do **not** immediately continue building the system.
Run a retrospective on that real execution first, and only change the pipeline if it exposes a
defect. Real usage is a better architect than speculation.

1. Which steps were unnecessary?
2. Which information was missing?
3. Which documents had to be edited manually?
4. What caused the longest delay?

## Validation acceptance criteria (first employment letter)

The first letter is a validation exercise, not a production milestone: its job is to prove v1.0
processes real evidence end-to-end without modification. Declare **Evidence Pipeline v1.0 validated
for employment-letter evidence** only if ALL hold after processing:

- [ ] The document is ingested without inventing facts.
- [ ] Every supported claim is traceable to evidence (Evidence ID).
- [ ] Unsupported claims remain `Pending`.
- [ ] All downstream artifacts regenerate without inconsistency (ER → AL → Timeline → Portfolio → CV status → LinkedIn).
- [ ] No manual edits are required outside the documented SOP.
- [ ] No framework changes are required during processing.

Wording matters: one successful employment letter validates the pipeline **for that evidence type
only**. Do not claim the pipeline is "validated" in general — PGCE certificates, testimonials,
classroom artefacts and other sources may expose different issues later. Each evidence type is
validated on its own run.

## Operations report format

Post-freeze updates use a two-section operations report. This is **project documentation** — its
layout can change without altering memory. Keep Results (value) and Health (reliability) separate so
a healthy-but-idle process is never mistaken for progress.

**Results** — is the pipeline creating value?
- Evidence received: (list, or "none")
- Claims verified: (+N)
- Verification coverage: (verified / total, or "0 / TBD")
- Acquisition lead time: (request → received; "not started" / "n/a")
- Processing lead time: (received → claim verified; "n/a")

**Health** — is the pipeline itself reliable?
- Pipeline defects observed: (None / count; "none observed (awaiting first execution)" until a real doc runs)
- Framework changes: (None / description)
- Validation status: (not yet validated / "Employment-letter evidence: Validated" / etc.)

**When execution exposes a defect:**
- Pipeline defects observed: One
- Defect: (what real execution revealed)
- Action: Framework change proposed against v1.0: (description)
- Decision: Approved / Rejected

This format sets a high bar for framework change: every change must be justified by an *observed*
execution defect, not a hypothetical improvement.
