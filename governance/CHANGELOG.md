# CHANGELOG.md

**Repository:** Career OS (Private)
**Owner:** Mohammed Shehzad Khan
**Format:** Reverse chronological. Every entry must include: date, version bump type, author, and a description of what changed and why.

**Version Convention:** `profile_version` uses semantic versioning.
- **Major** bump: role added, removed, or significantly reworded
- **Minor** bump: new skill, metric, narrative section, or governance document added
- **Patch** bump: wording correction, typo fix, date clarification, or internal flag change

---

## [Unreleased] — Career OS v4.0

### 2026-07-30 — Week 1 Execution (profile_version: 1.0.0-alpha)

**Author:** Claude Code (Antigravity)
**Type:** Major — repository restructure and governance foundation

#### Added
- `governance/` directory with full governance suite:
  - `Career_Taxonomy.md` — 12-field formal taxonomy (v1.0)
  - `DECISION_LOG.md` — v2.0, decisions D-001 through D-007
  - `TECHNICAL_DEBT.md` — v1.0, items TD-001 through TD-009
  - `EVIDENCE_GAP_REGISTER.md` — v1.0, gaps G-001 through G-008
  - `CHANGELOG.md` — this file (v1.0)
- `application_strategies/` directory:
  - `STRATEGY_A_PREMIUM.md` — Premium International Schools
  - `STRATEGY_B_MID_TIER.md` — Mid-Tier International Schools
  - `STRATEGY_C_TRAINER.md` — Teacher Training and Development
- `evidence/` directory scaffold with subdirectories: `credentials/`, `employment/`, `research/`, `references/`
- `evidence/manifest.yml` — skeleton (paths and descriptions; checksums deferred to Week 2 end)
- `career-data/facts/` directory (empty; to be populated in Week 2)
- `career-data/narratives/` directory (empty; to be populated in Week 2)
- `schemas/facts/` and `schemas/narratives/` directories (empty; to be populated in Week 2)
- `tests/` directory (empty; test modules to be written in Week 3)
- `recruiter_packs/` directory with 7 context subdirectories

#### Archived
- `mo-portfolio/` → `archive/portfolio-v1/`
- `mo-portfolio-backup-20260717-1827/` → `archive/portfolio-v1-backup-20260717/`
- `mo-portfolio-v2-backup-20260717-2014/` → `archive/portfolio-v2-backup-20260717/`
- `portfolio-v3/` → `archive/portfolio-v3-draft/`
- `public_portfolio/` → `archive/public-portfolio-draft/`
- `project-meridian/` → `archive/project-meridian/`

#### Fixed
- `mo-portfolio-v2/.github/workflows/deploy.yml` — branch trigger updated from `master` to `main` (Decision D-007; TD-007 resolved)

#### Governance Decisions
- D-003: Harris University listing policy confirmed (factual; per-document publication flags)
- D-004: PGCE described as non-QTS explicitly
- D-005: "4 schools" used as primary institutional count metric
- D-006: "International Primary Educator" confirmed as portfolio display title
- D-007: `main` confirmed as canonical deployment branch

---

*(Previous entries will be added as weeks progress)*

---

## Release History

| Release | Date | profile_version | Notes |
|---|---|---|---|
| Week 1 complete | 2026-07-30 | 1.0.0-alpha | Repository restructure and governance only |
| Week 2 complete | TBD | 1.0.0-beta | Canonical data model and evidence system |
| Week 3 complete | TBD | 1.0.0-rc | Generators and QA pipeline |
| v1.0.0 | TBD | 1.0.0 | Full release — portfolio live, all CVs generated |
