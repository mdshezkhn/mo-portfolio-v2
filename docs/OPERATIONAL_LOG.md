# Operational Validation — Season 1

This log captures real-world application outcomes to serve as the empirical dataset for improving the compiler architecture, policies, and canonical evidence base. Every application is treated as a controlled experiment.

## Season 1 Success Criteria & Exit Conditions

| Metric                               |           Baseline |       Season 1 Target |
| ------------------------------------ | -----------------: | --------------------: |
| Manual edits after generation        |             Record |  Reduce substantially |
| Time to produce tailored application |             Record |  Reduce substantially |
| Internal consistency defects         |                  0 |            Maintain 0 |
| Unsupported rendered claims          |                  0 |            Maintain 0 |
| Recruiter callback rate              | Establish baseline | Improve over baseline |
| Interview invitation rate            | Establish baseline | Improve over baseline |
| Offer quality & School fit           | Establish baseline | Optimize for long-term|
| System maintenance cost (hours)      | Establish baseline | Decrease over time    |

**Season 1 Exit Criteria:**
Season 1 will officially conclude, and an evaluation of architectural changes (v1.1) will occur, *only* when the following conditions are met:
1. A predetermined target number of pilot applications across core target markets (e.g., 10-15 applications) have been submitted.
2. The operational log is fully completed for every submission.
3. At least one full comprehensive review of accumulated evidence has been completed.
4. An explicit decision point is reached on whether the collected data justifies any v1.1 architectural work.

## Planned Experiments

| Experiment | Variable Changed | Success Measure |
|---|---|---|
| **E-001** | Baseline compiler output (Best genuine v1.0 baseline without experimental tuning) | Establish baseline benchmark metrics (H₀) |
| **E-002** | One policy or claim-selection change | Compare against E-001 |
| **E-003** | One presentation change (if justified) | Compare against E-002 |

### E-001 Pilot Design
The E-001 baseline must not be a "straw man." It represents the best artifact the v1.0 compiler can produce *without* experimental tuning. To establish this baseline, E-001 will consist of a deliberately small, regionally balanced pilot:
- **China (British/International):** 3 applications
- **Gulf (British/International):** 3 applications
- **Southeast Asia (British/International):** 3 applications

**CRITICAL: Lock the Baseline**
Before the first E-001 application is submitted, an immutable archival record must be created and preserved (never overwritten or "fixed" later). This record must include:
* Compiler version
* Canonical revision
* Policy version
* Generated artifacts
* Quality report
* Decision log
* Provenance verification result

## Operational Principles

1. **Establish the Baseline First:** Run E-001 completely (all 9 pilot applications) using *exactly* the same compiler version, canonical revision, and policy version. Do not optimize or tweak mid-pilot based on isolated anecdotes. Wait for the full baseline sample to complete to identify true patterns.
2. **The Null Hypothesis (H₀):** Every experiment assumes the modification has *no meaningful effect* on outcomes. You must gather enough evidence to reject H₀. If you can't, the conclusion is **No Change**.
3. **Data Sparsity & Confounding Variables:** International hiring is low volume with many external dependencies (visa, hiring season). Treat early findings as directional, not definitive, and always record external context.
4. **Regression Discipline:** When a successful application is found, resist the urge to change the system again. Stable periods are necessary to prove repeatability.
5. **Keep Experiments Small:** Change only one variable at a time (e.g., *only* alter the selection policy, *or* rewrite claims, but not both simultaneously).
6. **Embrace Negative Evidence:** Records where "We expected X, and it didn't happen" are extremely valuable for eliminating plausible explanations.
7. **Protect Against Survivorship Bias:** Record *every* application generated, regardless of outcome (including auto-rejections or silence).
8. **Unit of Analysis:** When reviewing an outcome, do not ask "Did this CV work?" Ask "Which change from the previous version plausibly contributed to the outcome?"
9. **Explicit Outcomes:** Every experiment must conclude with exactly one of these actions: Adopt, Reject, or No Change.

## Entry Template

```markdown
### Application: [Target School/Role]
- **Date:** YYYY-MM-DD
- **Target Market/Policy:** e.g., british_v1.0
- **Null Hypothesis (H₀):** (e.g., Leadership-focused claim ordering has no effect on response rate.)
- **Expected Outcome (Alternative Hypothesis):** (e.g., More interview invitations than the baseline policy.)
- **Compiler Version:** (e.g., v1.0.0)
- **Canonical Revision:** (Date/Hash of Canonical Graph)
- **Artifact Version:** (Commit Hash or Build ID)
- **Selected Claims:** (List of primary claim IDs generated)
- **External Context:** (e.g., Timing in season, visa requirements, regional conditions, role seniority)
- **Outcome:** Pending / No Response / Auto-Reject / Late Reject / Interview / Offer / Declined Offer
- **Recruiter Feedback:** (Objective patterns across reviewers; resist single-anecdote overfitting)
- **Conclusion:** Adopt / Reject / No Change
- **Actions Taken:** (e.g., Added evidence E-4001, or 'None')
- **Maintenance Cost:** (e.g., 2 hours spent updating canonical data for this application)
```

---

## Log Entries

*(Begin logging real-world applications here)*
