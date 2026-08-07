# Phase 0: Dependency Verification Report

## 1. Objective
Before migrating any architecture or deprecating any assets, we must formally establish the exact dependencies (producers and consumers) for every major directory and file in the repository.

**Classification States:**
* **Verified** — Producer exists and is documented within the repository.
* **External** — Producer is known but intentionally outside the repository.
* **Unknown** — Producer cannot yet be identified from repository evidence.
* **Manual** — Human-maintained by design (no programmatic producer).

---

## 2. Dependency Matrix

| Object | Producer | Consumer(s) | Entry Point | Evidence | Confidence | Status |
|---|---|---|---|---|---|---|
| `compiled_assets/` | `build.py` | Humans / Deployment | `career.py build` (Manual CLI) | `build.py:35` | High | **Verified** |
| `recruiter_packs/` | `generate_recruiter_pack.py` | None | None found (Script is orphaned) | `generate_recruiter_pack.py:22` | High | **Verified** |
| `career-data/computed/` | Unknown | Repository manifests | None found | Manifest references | Low | **Unknown** |
| `career-data/golden/` | Unknown / Historical | Repository manifests | None found | `manifest.json` | Low | **Unknown** |
| `career-data/view_models/` | Unknown | `generate_recruiter_pack.py` | None found | `generate_recruiter_pack.py:31` | Low | **Unknown** |
| `artifacts/professional_profile_vm.json`| `scripts/build_view_models.py` | `scripts/render_markdown.py` | `scripts/ci_pipeline.py` | `build_view_models.py:132` | High | **Verified** |
| `templates/cv/profiles/*.json` | Humans | `build.py` | Manual edit | JSON files tracked directly in Git | High | **Manual** |
| `mo-portfolio-v2/index.html` | Humans | GitLab Pages | Manual edit | Static file, no generator script | High | **Manual** |
| `evidence/manifest.yml` | Humans | `validate_evidence.py`, `ci_pipeline.py` | Manual edit | `test_evidence_dependencies.py:8` | High | **Manual** |
| `career-data/facts/*.yml` | Humans | `validate_yaml.py`, `resolve_graph.py` | Manual edit | `ci_pipeline.py` | High | **Manual** |

---

## 3. Analysis & Phase 0 Conclusions

### 3.1. The "Unknown" Objects
* `career-data/computed/`
* `career-data/golden/`
* `career-data/view_models/`

**Verdict:** These directories have absolutely no in-repository producer. They are not managed by the current build system. However, they cannot be safely deleted until we verify they are not required by an **External** system or manual recruiter workflow outside of Git.

### 3.2. The "Manual" Deployment Objects
* `templates/cv/profiles/*.json`
* `mo-portfolio-v2/index.html`

**Verdict:** The primary deployment payload (`mo-portfolio-v2/index.html`) and the primary recruiter CVs (built from `templates/cv/profiles/*.json`) are currently **Manual**. There is zero in-repository automation driving them from the canonical `career-data/facts/`. This formally validates the core architectural flaw.

### 3.3. The "Verified" (But Orphaned) Objects
* `recruiter_packs/`
* `generate_recruiter_pack.py`

**Verdict:** The script exists in the repository, making the producer **Verified**. However, it is an orphan because it has no Entry Point (it is never invoked by CI or CLI) and it consumes an input directory (`career-data/view_models/`) whose status is **Unknown**.

---

## 4. Phase 0 Gate Check

> **Exit Criteria Met? YES.**
> Every directory and file now has an explicit status of Verified, Manual, External, or Unknown.

With these dependencies formally mapped, we have proven exactly which parts of the repository are governed by automation and which rely on manual synchronization. We are now cleared to proceed to **Phase 1: Build Graph Documentation** and **Phase 2: Single Canonical View Model**.
