# Phase 4: Complete Provenance Reconstruction (Evidence Only)

## 1. Build Entry Points
A comprehensive scan of the repository for build scripts, package managers, and automation wrappers reveals the following actual entry points:

- **`scripts/ci_pipeline.py`**: The primary CI orchestrator. Executes 23 sequential stages of python scripts and tests.
- **`.github/workflows/build.yml`**: GitHub Actions workflow. Runs `ci_pipeline.py` (implicitly via its stages), `generate_manifest.py`, `prove_determinism.py`, and `npm run build`.
- **`package.json`**: NPM scripts. The `build` script is a mock (`node -e "console.log('Static site, no build step required.');..."`). It does not compile assets.
- **`career.py`**: CLI wrapper. Defines `run_build()` which calls `build.py`.
- **`build.py` (Root Level)**: A standalone python script that consumes `templates/cv/profiles/*.json` and generates outputs in `compiled_assets/`.
- **`mo-portfolio-v2/.gitlab-ci.yml`**: Deployment orchestrator for the public site.

## 2. Trace Every Output

| Generated Directory | Created By Script | Function | Line | Outputs |
|---|---|---|---|---|
| `compiled_assets/` | `build.py` | `main()` | L35 | HTML/MD CVs and Portfolios |
| `artifacts/professional_profile_vm.json` | `scripts/build_view_models.py` | `main` block | L132 | JSON View Model |
| `artifacts/generated/cv.md` | `scripts/render_markdown.py` | `main` block | L65 | Markdown CV |
| `career-data/intermediate/` | `scripts/compile_intermediate.py`, `scripts/resolve_graph.py` | Argparse `--output-dir` | L62, L213 | JSON Graphs |
| `mo-portfolio-v2/assets/images/certificates/` | `scripts/process_authentic_certificates.py`, `scripts/generate_documentary_certificates.py` | Global / `main` | L8, L6 | Images/PDFs |
| `career-data/view_models/` | **UNKNOWN** | **UNKNOWN** | N/A | **UNKNOWN** |
| `career-data/computed/` | **UNKNOWN** | **UNKNOWN** | N/A | **UNKNOWN** |
| `career-data/golden/` | **UNKNOWN** (Release Snapshots) | **UNKNOWN** | N/A | **UNKNOWN** |
| `recruiter_packs/` | **UNKNOWN** | **UNKNOWN** | N/A | **UNKNOWN** |

## 3. Reverse Dependency Graph (Verified Only)

**Pipeline 1: The Automated CI Pipeline (artifacts/)**
```text
career-data/facts/*.yml (Human Authored)
        │
scripts/build_view_models.py
        │
        ▼
artifacts/professional_profile_vm.json
        │
scripts/render_markdown.py
        │
        ▼
artifacts/generated/cv.md
```

**Pipeline 2: The Manual Build Pipeline (compiled_assets/)**
```text
templates/cv/profiles/*.json (Human Authored? No provenance found for these JSONs)
templates/cv/base.html
        │
build.py (Run manually via `python career.py build`)
        │
        ▼
compiled_assets/CV_*.html, Portfolio_Copy.md
```

**Pipeline 3: The Deployment Pipeline (mo-portfolio-v2/)**
```text
mo-portfolio-v2/index.html (Human Authored)
mo-portfolio-v2/assets/* (Human Authored / Manually Copied)
        │
.gitlab-ci.yml (cp -r ...)
        │
        ▼
GitLab Pages (Production)
```

## 4. Dead Asset Detection

| Directory / Script | Referenced By | Status | Justification |
|---|---|---|---|
| `career-data/view_models/` | `generate_recruiter_pack.py` | **DEAD/ORPHAN** | Read by a script, but never written to. |
| `career-data/computed/` | `manifest.json`, Index MDs | **ORPHAN** | Mentioned in docs/manifests, but no script generates it. |
| `generate_recruiter_pack.py` | None | **DEAD** | Never called in CI, CLI, or other scripts. |
| `templates/cv/profiles/*.json`| `build.py` | **ACTIVE (Manual)** | Manually maintained inputs to a manual script. |
| `recruiter_packs/` | None | **ORPHAN** | Never generated. |

## 5. Build Pipeline Reconstruction

**The Observed Automated Pipeline (`ci_pipeline.py` & `.github/workflows/build.yml`):**
```text
career-data/facts/*.yml
↓
validate_yaml.py (Validation)
↓
resolve_graph.py (Outputs to intermediate/)
↓
compile_intermediate.py (Outputs to intermediate/)
↓
build_view_models.py (Outputs to artifacts/professional_profile_vm.json)
↓
render_markdown.py (Outputs to artifacts/generated/cv.md)
↓
Tests & Validation Gates
```
*(Note: `build.py` is entirely missing from the automated pipeline)*

## 6. Deployment Trace
How do files reach `mo-portfolio-v2/`?
* **Answer:** **Manual Copy / Direct Human Editing.**
* **Evidence:** There is absolutely zero automation connecting `compiled_assets/` (or `artifacts/generated/`) to `mo-portfolio-v2/`. `mo-portfolio-v2/index.html` is manually edited. `build.py` and the `ci_pipeline.py` do not emit to `mo-portfolio-v2/`. The only automated deployment is `.gitlab-ci.yml` which deploys whatever is currently committed in the `mo-portfolio-v2/` folder.

## 7. CI Coverage
**Scripts Executed by CI:**
`audit_claims.py`, `validate_ids.py`, `validate_yaml.py`, `resolve_graph.py`, `validate_semantics.py`, `metrics_engine.py`, `content_quality_engine.py`, `selection_engine.py`, `compile_claim_register.py`, `compile_intermediate.py`, `policy_engine.py`, `build_view_models.py`, `render_markdown.py`, `verify_cross_artifact.py`, `build_compiler_report.py`, `generate_manifest.py`, `prove_determinism.py`, `audit_manifest.py`

**Scripts NOT Executed by CI (Manual/Dead):**
`build.py`, `career.py`, `generate_recruiter_pack.py`, `process_authentic_certificates.py`, `generate_documentary_certificates.py`, `generate_schemas.py`

## 8. Provenance Matrix

| Directory / Artifact | Producer | Consumer | Evidence | Confidence | Status |
|---|---|---|---|---|---|
| `compiled_assets/` | `build.py` | Manual copy to deployment | `build.py` L35, L81 | High | **Verified** |
| `artifacts/professional_profile_vm.json` | `scripts/build_view_models.py` | `render_markdown.py` | `build_view_models.py` L132 | High | **Verified** |
| `artifacts/generated/` | `scripts/render_markdown.py` | None | `render_markdown.py` L65 | High | **Verified** |
| `career-data/intermediate/` | `scripts/resolve_graph.py` | `scripts/build_view_models.py` | `resolve_graph.py` argparse | High | **Verified** |
| `career-data/computed/` | Unknown | Unknown | None | Low | **Unsupported** |
| `career-data/view_models/` | Unknown | `generate_recruiter_pack.py` | None | Low | **Unsupported** |
| `mo-portfolio-v2/` | Humans | `.gitlab-ci.yml` | Git history, lack of scripts | High | **Derived** |

## 9. Repository Health
- **Dead Generators:** `generate_recruiter_pack.py` consumes missing directories.
- **Unreachable Outputs:** `artifacts/generated/cv.md` is generated by CI but never deployed. `compiled_assets/` is built manually but never deployed automatically.
- **Unreachable Sources:** `templates/cv/profiles/*.json` have no provenance; they appear to be manually maintained JSON files mirroring YAML data.
- **Duplicate Pipelines:** The repo maintains two separate rendering pipelines. Pipeline 1 (`build_view_models.py` -> `render_markdown.py`) runs in CI. Pipeline 2 (`build.py` -> `compiled_assets/`) runs manually.

## 10. Final Verdict
1. **Verified architecture:** The CI pipeline validates facts and builds `artifacts/`. The manual `build.py` builds `compiled_assets/`.
2. **Unsupported architecture:** `career-data/computed/` and `career-data/view_models/` do not exist in the automation layer.
3. **Unknown provenance:** How `templates/cv/profiles/*.json` are generated, and how `compiled_assets/` reaches the production site.
4. **Dead code:** `generate_recruiter_pack.py`.
5. **Dead directories:** `recruiter_packs/`.
6. **Manual processes:** Building `compiled_assets/` via `career.py build`, moving assets into `mo-portfolio-v2/`.
7. **Automated processes:** Fact validation, schema checks, determinism proofs, and deployment of whatever is statically in `mo-portfolio-v2/`.
8. **Build bottlenecks:** Disconnect between the CI-verified artifacts and the actual deployed HTML files.
9. **Missing provenance:** The linkage between `career-data/facts/*.yml` and `mo-portfolio-v2/index.html`.
10. **Repository confidence score:** **6/10**. High confidence in the validation layer; zero confidence in the automated assembly of the deployment payload.
