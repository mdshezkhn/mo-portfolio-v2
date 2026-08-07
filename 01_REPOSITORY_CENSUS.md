# Repository Census: Mo Digital Portfolio

## 1. Executive Summary
This forensic census documents the structure and purpose of two distinct Git repositories found within the workspace. 
- **Repository A (mo-portfolio-v2):** Appears to be the Production Portfolio containing deployment assets, HTML/JS/CSS, and lighthouse reports.
- **Repository B (Workspace Root - release/2027.1):** Functions as a "Career OS" holding the canonical data (YAML/JSON facts), schemas, templates, build scripts, governance policies, and raw evidence used to generate the artifacts in Repository A and other recruiter packs.

## 2. Top-Level Directory Inventory

### Repository B (Career OS)
- **career-data**: Contains the source of truth for facts, metrics, and relationships, as well as intermediate and golden records.
- **schemas**: Defines the JSON schemas for claims, evidence, and manifest validation.
- **scripts**: Contains python scripts representing the build system, analytics, auditing, and generation pipelines.
- **templates**: Contains HTML and MD templates used for generating CVs and portfolio copies.
- **evidence**: Contains manifest and hash references for evidence validation.
- **EVIDENCE_LIBRARY**: Contains private and indexed evidence files (e.g., certificates, letters).
- **governance**: Houses policies, architectures, rules, and audit logs.
- **compiled_assets**: Holds the generated HTML and MD CVs and portfolio outputs.
- **artifacts**: Contains build outputs, metrics history, and compiler reports.
- **recruiter_packs**: Contains generated packages for external recruiters.
- **docs**: Documentation related to the Career OS architecture and operation.
- **registry**: Contains global ID mappings (e.g., ids.yml).
- **releases**: Historical release zip artifacts.
- **tests**: Test suites.
- **temp_certs**: Temporary generated certificates.
- **private**: Internal material.
- **archive / mo-portfolio / mo-portfolio-v2-backup-***: Backups and legacy directories.

### Repository A (Production Portfolio - `mo-portfolio-v2`)
- **assets**: Production CSS, JS, images, fonts, etc.
- **_qa_shots**: QA screenshots of the UI.
- **docs**: Documentation for the web deployment.
- **archive / backups**: Backups specific to the web deployment.

## 3. Classification Table

| Directory | Category | Authority | Lifecycle | Deploy | Rebuildable | Priority | Confidence |
|---|---|---|---|---|---|---|---|
| `career-data` | CANONICAL_SOURCE | YES | SOURCE | NO | NO | KEEP | High |
| `schemas` | CANONICAL_SOURCE | YES | SOURCE | NO | NO | KEEP | High |
| `scripts` | BUILD_SYSTEM | YES | SOURCE | NO | NO | KEEP | High |
| `templates` | CANONICAL_SOURCE | YES | SOURCE | NO | NO | KEEP | High |
| `evidence` | EVIDENCE | YES | SOURCE | NO | NO | KEEP | High |
| `EVIDENCE_LIBRARY` | EVIDENCE | PARTIAL | SOURCE | NO | NO | KEEP | High |
| `governance` | GOVERNANCE | YES | SOURCE | NO | PARTIAL | KEEP | High |
| `registry` | CANONICAL_SOURCE | YES | SOURCE | NO | NO | KEEP | High |
| `compiled_assets` | GENERATED | NO | GENERATED | NO | YES | REGENERATE | High |
| `artifacts` | GENERATED | NO | GENERATED | NO | YES | REGENERATE | High |
| `recruiter_packs` | GENERATED | NO | GENERATED | NO | YES | REGENERATE | High |
| `releases` | ARCHIVE | NO | HISTORICAL | NO | YES | ARCHIVE | High |
| `temp_certs` | TEMPORARY | NO | GENERATED | NO | YES | ARCHIVE | High |
| `private` | PRIVATE | PARTIAL | SOURCE | NO | NO | REVIEW | Medium |
| `archive` | ARCHIVE | NO | HISTORICAL | NO | NO | ARCHIVE | High |
| `mo-portfolio` | ARCHIVE | NO | HISTORICAL | NO | NO | ARCHIVE | High |
| `mo-portfolio-v2-backup-*` | BACKUP | NO | HISTORICAL | NO | NO | ARCHIVE | High |
| `mo-portfolio-v2/assets` | DEPLOYMENT | YES | SOURCE | YES | NO | KEEP | High |
| `mo-portfolio-v2/_qa_shots` | EVIDENCE | NO | GENERATED | NO | YES | ARCHIVE | Medium |
| `mo-portfolio-v2/backups` | BACKUP | NO | HISTORICAL | NO | NO | ARCHIVE | High |

## 4. Duplicate Trees
- **`archive` vs `mo-portfolio-v2-backup-20260717-2014` vs `mo-portfolio-v2/archive`**: Multiple overlapping backup/archive directories exist across the repositories.
- **`mo-portfolio`**: A legacy directory that appears to be a stub or duplicate of earlier workspace roots.
- **`evidence` vs `EVIDENCE_LIBRARY`**: `evidence` contains `hashes.yml` and `manifest.yml`, while `EVIDENCE_LIBRARY` contains the actual indexed files and a `private` subdirectory.

## 5. Generated vs Source Matrix
- **Sources (Do Not Delete):** `career-data`, `schemas`, `templates`, `scripts`, `governance`, `evidence`, `EVIDENCE_LIBRARY`, `registry`, `mo-portfolio-v2/assets`.
- **Generated (Safe to Delete/Rebuild):** `compiled_assets`, `artifacts`, `recruiter_packs`, `temp_certs`, release zip files.

## 6. Source Authority Matrix
- **career facts:** `career-data/facts`, `career-data/golden` (Authoritative)
- **employment:** `career-data/facts` (Authoritative)
- **education:** `career-data/facts` (Authoritative)
- **evidence:** `evidence/manifest.yml` for metadata/hashes, `EVIDENCE_LIBRARY` for physical files.
- **templates:** `templates/` (Authoritative)
- **portfolio assets:** `mo-portfolio-v2/assets/` (Authoritative)
- **compiled outputs:** None. The outputs in `compiled_assets` are generated artifacts.
- **governance:** `governance/` (Authoritative)
- **schemas:** `schemas/` (Authoritative)
- **validation:** `schemas/` and Python verification logic in `scripts/`.

## 7. Deployment Boundary
The deployment boundary strictly separates the "Career OS" data layer from the "Production Portfolio" presentation layer.
- **Included in Deployment:** `mo-portfolio-v2/assets`, `mo-portfolio-v2/index.html`, `mo-portfolio-v2/live_index.html`.
- **Excluded from Deployment:** ALL Career OS directories (`career-data`, `schemas`, `scripts`, `governance`, `artifacts`, etc.). These exist only to build, validate, and compile the final outputs that are then handed over to the deployment boundary.

## 8. Risk Observations
- Multiple backup and archive folders (`mo-portfolio-v2-backup-*`, `archive`, `mo-portfolio`) create confusion around the single source of truth for historical data.
- The separation between `evidence` (metadata/hashes) and `EVIDENCE_LIBRARY` (files) could lead to synchronization issues if not managed properly by the build scripts.
- Private materials are scattered (`private/`, `EVIDENCE_LIBRARY/private/`).
- The Production Portfolio (`mo-portfolio-v2`) is nested inside the Career OS Repository, which can cause Git submodule/nested-repo confusion.

## 9. Questions that must be answered BEFORE any migration
1. Are the historical backups (`mo-portfolio-v2-backup-*`, `archive`) required to be migrated, or can they be permanently archived externally?
2. Should the Production Portfolio (`mo-portfolio-v2`) remain a nested directory, or should it be separated into a completely independent path structure?
3. What is the precise workflow bridging the output of `compiled_assets` to the `mo-portfolio-v2` deployment?
4. Is `mo-portfolio` (legacy stub) entirely safe to remove?

## 10. Recommendations
- **KEEP:** `career-data`, `schemas`, `scripts`, `templates`, `evidence`, `EVIDENCE_LIBRARY`, `governance`, `registry`, `mo-portfolio-v2/assets`.
- **REVIEW:** `private` (to determine if contents should be integrated into `EVIDENCE_LIBRARY/private` or governance).
- **REGENERATE:** `compiled_assets`, `artifacts`, `recruiter_packs`, `temp_certs`.
- **ARCHIVE:** `releases`, `archive`, `mo-portfolio`, `mo-portfolio-v2-backup-*`, `mo-portfolio-v2/_qa_shots`, `mo-portfolio-v2/backups`.
