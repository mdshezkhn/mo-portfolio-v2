# Release Reproducibility Audit (Phase 5)

## 1. Core Audit Question
> **Can the deployed portfolio (`mo-portfolio-v2`) be reproduced bit-for-bit from the canonical facts using only repository automation?**

**Answer: NO.**

The repository fails the release reproducibility requirement. The evidence proves there is a structural airgap between the canonical data sources and the deployment payload.

## 2. Reproducibility Assessment

| File / Component | Reproducible from Canonical Data? | Automation Path | Evidence |
|---|---|---|---|
| `mo-portfolio-v2/index.html` | **No (Manual)** | None | No scripts in the repository output to this path. It is tracked as a static file in Git. |
| `mo-portfolio-v2/assets/css/` | **No (Manual)** | None | No CSS preprocessors or build scripts output to this path. |
| `mo-portfolio-v2/assets/js/` | **No (Manual)** | None | No bundlers or compilers output to this path. |
| `mo-portfolio-v2/assets/images/certificates/`| **Yes (Partial)** | `process_authentic_certificates.py`, `generate_documentary_certificates.py` | Scripts write directly to this directory based on canonical data. |
| `compiled_assets/CV_*.html` | **No (Manual Inputs)** | `build.py` consumes `templates/cv/profiles/*.json` | There is no script connecting the canonical YAML facts to the JSON profiles required by `build.py`. |
| `artifacts/generated/cv.md` | **Yes** | `build_view_models.py` -> `render_markdown.py` | Complete end-to-end automation from canonical YAML to final Markdown artifact. |

## 3. Evidence of the "Two Truths" Flaw

The repository currently maintains two structurally disconnected pipelines, destroying the Single Source of Truth invariant.

**Pipeline A (The Validated Truth)**
- **Source:** `career-data/facts/*.yml`
- **Automation:** `ci_pipeline.py` -> `build_view_models.py` -> `render_markdown.py`
- **Output:** `artifacts/generated/cv.md`
- **Deployment Status:** **Never Deployed.** (Stays in the `artifacts/` folder).

**Pipeline B (The Deployed Truth)**
- **Source:** `templates/cv/profiles/*.json` (No generator found. Must be manually maintained).
- **Automation:** `build.py` (Manual CLI execution. Not in CI).
- **Output:** `compiled_assets/CV_*.html`
- **Deployment Status:** **Partially Deployed.** (Outputs are manually copied to the recruiter or the web portfolio; there is no automated bridge to `mo-portfolio-v2/`).

**Pipeline C (The Web Portfolio)**
- **Source:** `mo-portfolio-v2/index.html` (No generator found. Contains hardcoded facts).
- **Automation:** `.gitlab-ci.yml` (Copies static files verbatim to the GitLab Pages public folder).
- **Output:** The live website.
- **Deployment Status:** **Fully Deployed, but unverified.**

## 4. Repository Scorecard

| Area | Status |
|---|---|
| Canonical data provenance | **Verified** (`career-data/facts/`) |
| Validation pipeline | **Verified** (`ci_pipeline.py`) |
| Artifact generation | **Verified** (`artifacts/generated/`) |
| Deployment provenance | **No in-repository producer identified** |
| Recruiter pack provenance | **No in-repository producer identified** |
| View model provenance (`career-data/view_models/`) | **No in-repository producer identified** |
| Computed data provenance (`career-data/computed/`) | **No in-repository producer identified** |
| End-to-end deterministic release | **Not demonstrated** |

## 5. Final Reproducibility Verdict

The repository **cannot** produce its published artifacts from source in a deterministic, verifiable way. 

The deployed web portfolio (`mo-portfolio-v2/index.html`) and the intermediate recruiter artifacts (`compiled_assets/`) require manual intervention and manual data synchronization. Any changes made to the canonical YAML facts will **not** propagate to the live website or the compiled HTML CVs without a human manually updating the corresponding JSON profiles and HTML structures.
