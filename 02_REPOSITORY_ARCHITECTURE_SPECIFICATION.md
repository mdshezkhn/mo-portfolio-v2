# Repository Architecture Specification: Mo Digital Portfolio

## 1. Executive Summary
This document establishes the production-grade architectural baseline for the Mo Digital Portfolio repositories. It transitions from a basic forensic census to a prescriptive, canonical map of the system's architecture, defining golden records, build provenance, deployment boundaries, and repository governance rules. It is descriptive of the current state and highlights structural patterns that will inform future refactoring and migration.

---

## Phase 1 — Canonical Source Analysis

| Directory | Classification | Confidence |
|---|---|---|
| `career-data/facts/` | Canonical Source | High |
| `career-data/relationships/` | Canonical Source | High |
| `career-data/legacy/` | Archive | High |
| `career-data/computed/` | Generated | High |
| `career-data/intermediate/` | Temporary | High |
| `career-data/view_models/` | Generated | High |
| `career-data/golden/` | Canonical Source / Generated (Mixed) | Medium |
| `templates/cv/` | Canonical Source | High |
| `mo-portfolio-v2/assets/css/` | Canonical Source | High |
| `mo-portfolio-v2/assets/images/` | Canonical Source | High |
| `mo-portfolio-v2/assets/js/` | Canonical Source | High |
| `evidence/` | Canonical Source | High |
| `EVIDENCE_LIBRARY/` | Canonical Source (Physical Files) | High |

---

## Phase 2 — Golden Record Mapping

| Domain | Canonical Path | Confidence | Reason |
|---|---|---|---|
| Employment | `career-data/facts/employment.yml` | High | Human-authored YAML source. |
| Education | `career-data/facts/education.yml` | High | Human-authored YAML source. |
| Claims/Metrics | `career-data/facts/claims.yml` | High | Central registry of verified facts. |
| Evidence Metadata | `evidence/manifest.yml`, `hashes.yml` | High | Central validation registry for assets. |
| Governance | `governance/` | High | Policies and architectures baseline. |
| Templates | `templates/` | High | Source files for CV/Portfolio generation. |
| Registry | `registry/ids.yml` | High | Global identifier definitions. |
| Portfolio Assets | `mo-portfolio-v2/assets/` | High | Deployment-ready CSS/JS/images. |

---

## Phase 3 — Provenance Analysis

### `compiled_assets/`
* **Produced by:** `scripts/render_markdown.py`, `scripts/build_view_models.py`
* **Consumes:** `career-data/view_models/`, `templates/`
* **Outputs:** HTML, Markdown, PDF (CVs and Portfolios)
* **Rebuild Command:** `scripts/ci_pipeline.py`
* **Deterministic:** Yes (verified by `scripts/prove_determinism.py`)
* **Safe to delete:** Yes

### `career-data/view_models/`
* **Produced by:** `scripts/build_view_models.py`
* **Consumes:** `career-data/facts/`, `career-data/relationships/`
* **Outputs:** JSON view models for templates
* **Rebuild Command:** `scripts/build_view_models.py`
* **Deterministic:** Yes
* **Safe to delete:** Yes

### `artifacts/`
* **Produced by:** Build and validation scripts
* **Consumes:** Test runs, audit executions, metrics engine
* **Outputs:** JSON manifests, logs, compiler reports
* **Rebuild Command:** `scripts/ci_pipeline.py`
* **Deterministic:** Yes
* **Safe to delete:** Yes

---

## Phase 4 — Build Dependency Graph

```text
Human Authored Data (career-data/facts/, registry/)
       │
       ▼
[ Data Validation Layer (scripts/validate_schemas.py, schemas/) ]
       │
       ▼
[ View Model Generation (scripts/build_view_models.py) ]
       │
       ▼
career-data/view_models/
       │                  ┌── templates/
       ▼                  ▼
[ Presentation Generation (scripts/render_markdown.py) ]
       │
       ▼
compiled_assets/
       │
       ▼
mo-portfolio-v2/ (Deployment Boundary)
```

---

## Phase 5 — File Ownership

| Directory | Owner | Reason |
|---|---|---|
| `career-data/` | Career OS | Contains raw facts and data models. |
| `schemas/`, `scripts/` | Build System | Validation and build orchestration logic. |
| `evidence/`, `EVIDENCE_LIBRARY/` | Evidence Registry | Source of truth for physical and hashed evidence. |
| `governance/`, `audit/` | Governance | Compliance, policies, and system constitution. |
| `mo-portfolio-v2/` | Deployment | Presentation layer and static web hosting assets. |
| `tests/`, `_qa_shots/` | QA | Quality assurance and regression testing. |
| `releases/` | Release Engineering | Zipped distribution artifacts. |
| `archive/` | Historical Archive | Legacy documentation and backups. |

---

## Phase 6 — Duplication Analysis

### Backups and Archives
* **Duplicate:** `archive/`, `mo-portfolio-v2-backup-*`, `mo-portfolio-v2/archive/`
* **Canonical Copy:** Git history and `releases/`
* **Reason Duplicate Exists:** Manual file-system level backups taken before Git mastery.
* **Can Rebuild:** No (historical snapshots).
* **Migration Risk:** High. Confusion over the true historical source of truth.

### Evidence Separation
* **Duplicate:** `evidence/` vs `EVIDENCE_LIBRARY/`
* **Canonical Copy:** `evidence/` (for metadata), `EVIDENCE_LIBRARY/` (for physical binaries).
* **Reason Duplicate Exists:** Separation of concerns (hashes/manifest vs actual PDFs). Not a true duplicate, but poses synchronization risks.
* **Can Rebuild:** No.
* **Migration Risk:** Medium.

---

## Phase 7 — Mixed Directories

### `career-data/`
* **Mixed Directory:** Yes.
* **Source Files:** `facts/`, `relationships/`, `golden/`
* **Generated Files:** `view_models/`, `computed/`, `intermediate/`
* **Recommended Split:** Separate source data (`career-data-src/`) from build outputs (`career-data-build/`).
* **Risk:** High. Accidentally committing generated artifacts leading to merge conflicts and loss of deterministic builds.

---

## Phase 8 — Deployment Boundary

### Career OS Repository (Source & Build System)
* `career-data/`
* `schemas/`
* `scripts/`
* `templates/`
* `evidence/` & `EVIDENCE_LIBRARY/`
* `governance/`
* `registry/`
* `compiled_assets/` (Build output destined for deployment)
* `artifacts/`, `releases/`, `tests/`, `audit/`

### Deployment Repository (Production Portfolio)
* `mo-portfolio-v2/assets/`
* `mo-portfolio-v2/index.html`
* `mo-portfolio-v2/live_index.html`
* `mo-portfolio-v2/manifest.webmanifest`

*Rule: No files from Career OS should be deployed to production. Only the outputs generated by Career OS are injected into the Deployment Repository.*

---

## Phase 9 — Nested Repository Assessment

**Current State:**
```text
Career OS (Repository B)
    └── mo-portfolio-v2 (Repository A, contains .git)
```

**Assessment:**
* **Advantages:** Colocated code makes local testing and end-to-end building simple.
* **Disadvantages:** Submodule/nested Git hell. CI triggers are disjointed. Git history is detached. Risk of committing to the wrong repository.
* **Recommendation:** **Separate**. The Career OS should be an independent repository that runs a CI pipeline, builds the artifacts, and pushes them to a completely independent Deployment repository via a deployment action.

---

## Phase 10 — Risk Register

| Risk | Severity | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| **Nested Repositories** | High | High | Broken CI, detached HEADs, commit confusion. | Separate into two independent repositories. Link via CI/CD artifact passing. |
| **Mixed Source/Generated Dirs** | Medium | High | Committing `view_models/`, merge conflicts. | Enforce strict separation of `src/` and `build/`. Update `.gitignore`. |
| **Duplicate Archives** | Low | High | Clutter, confusion over historical truth. | Remove manual folder backups. Rely on Git tags/releases. |
| **Private Evidence Leak** | High | Low | Exposure of PII or private certificates. | Strict `.gitignore` rules on `EVIDENCE_LIBRARY/private/`, pre-commit hooks to scan for PII. |
| **Evidence Sync Failure** | Medium | Medium | Hashes in `manifest.yml` drift from physical files. | Automate hash updates and validation via CI checks. |

---

## Phase 11 — Repository Contracts

### `career-data/facts/`
* **Inputs:** Human-authored YAML/JSON.
* **Outputs:** Normalized YAML records.
* **Consumers:** `build_view_models.py`, `validate_schemas.py`.
* **Mutation Policy:** Manual authoring only. Must pass strict schema validation before commit.

### `compiled_assets/`
* **Inputs:** JSON view models, HTML/MD templates.
* **Outputs:** Rendered CVs and Portfolios.
* **Consumers:** Deployment pipeline, recruiters.
* **Mutation Policy:** Generated entirely by scripts. Manual edits are strictly forbidden and will be overwritten.

### `governance/`
* **Inputs:** Strategic decisions, audit rules.
* **Outputs:** Markdown policies, JSON rulesets.
* **Consumers:** Audit scripts, developers.
* **Mutation Policy:** Requires formal review. No automated mutation.

---

## Phase 12 — Repository Constitution

These rules form the immutable invariants of the repository architecture:

1. **Generated artifacts shall never become canonical.**
2. **Every generated artifact must declare provenance and be fully rebuildable deterministically.**
3. **Every canonical record shall exist exactly once (Single Source of Truth).**
4. **The deployment repository shall never contain governance policies or Career OS source data.**
5. **Evidence hashes (`manifest.yml`) must remain strictly synchronized with the physical files in `EVIDENCE_LIBRARY`.**
6. **Mixed source and generated directories must not exist. Outputs belong in isolated `build/` directories.**
7. **Historical archives are immutable; Git tags and release artifacts shall replace manual folder backups.**
8. **No manual edits shall be made to files residing within the deployment boundary if they are generated by the Career OS.**
