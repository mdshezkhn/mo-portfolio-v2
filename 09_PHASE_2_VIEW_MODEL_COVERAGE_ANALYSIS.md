# Phase 2: View Model Coverage Analysis

## 1. Objective
This document executes the Phase 2 dependency verification by performing a field lineage audit. The goal is to mathematically determine if the current `artifacts/professional_profile_vm.json` is functionally complete enough to become the sole canonical bridge between `career-data/facts/` and all downstream renderers.

---

## 2. Coverage Evaluation

| Check | Question | Result |
|---|---|---|
| **Data coverage** | Does the VM contain every canonical fact required downstream? | **FAIL.** Missing `competencies`, `subtitle`, and `asset_name`. |
| **Semantic coverage** | Does it preserve structure, relationships, IDs, formatting? | **FAIL.** Type mismatches (`summary` is a list instead of a string, `date` is split instead of concatenated). |
| **Consumer coverage** | Can every renderer consume only the VM? | **FAIL.** `build.py` cannot consume the VM without manual JSON profiles injecting the missing fields. |
| **Loss analysis** | What information disappears between facts → VM? | **FAIL.** Crucial geographical and operational data is dropped. |

---

## 3. Field Lineage Matrix

This matrix tracks the flow of data from `career-data/facts/*.yml` to the current View Model (`professional_profile_vm.json`), and evaluates its compatibility with the actual rendering consumers (e.g., `build.py` and `render_markdown.py`).

| Canonical Field (YAML) | VM Field (JSON) | Consumer(s) | Status | Notes / Justification |
|---|---|---|---|---|
| `employment.id` | `experience[].id` | CV, Recruiter | Preserved | Exact mapping. |
| `employer_id` (via graph) | `experience[].organization` | CV, Portfolio | Derived | Looked up canonical org name via `WORKED_AT`. Consumer expects `company`. |
| `role_id` (via graph) | `experience[].title` | CV, Portfolio | Derived | Looked up role title via `HAS_ROLE`. Exact match. |
| `dates.start` | `experience[].start_date` | CV, Portfolio | Split | Consumer (`build.py`) expects a single formatted string (`"Feb 2024 - Present"`). |
| `dates.end` | `experience[].end_date` | CV, Portfolio | Split | Consumer (`build.py`) expects a single formatted string. |
| **N/A** (Derived from Claims) | `experience[].highlights` | CV, Portfolio | Renamed | Consumer expects `bullets`. Derived dynamically via `SUPPORTED_BY` edges. |
| `physical_country` | — | None | **Dropped** | Dropped by `build_view_models.py`. Needed for Recruiter Packs. |
| `operational_regions` | — | None | **Dropped** | Dropped by `build_view_models.py`. Needed for Recruiter Packs. |
| `education.degree` | `education[].name` | CV, Portfolio | Renamed | Consumer (`build.py`) expects a list of flat strings, but VM provides dictionaries. |
| `claims` (Priority: High) | `executive_summary` | CV, Portfolio | Type Mismatch | VM provides a `list`. Consumers expect a concatenated paragraph `string`. |
| `claims` (List) | `key_claims` | None | Type Mismatch | Consumer expects `claims` as an array of IDs or concise strings. |
| **MISSING IN VM** | `competencies` | CV, Portfolio | **Missing** | The VM generator completely drops competency tagging. Requires manual injection. |
| **MISSING IN VM** | `subtitle` | CV | **Missing** | Hardcoded in legacy manual JSONs. |
| **MISSING IN VM** | `asset_name` | CV | **Missing** | Hardcoded in legacy manual JSONs. |

---

## 4. Quantitative Metrics

| Metric | Value | Target | Status |
|---|---:|---:|---|
| **Canonical Coverage** | **65%** | 100% | The VM drops geographic data, competencies, and exact date strings. |
| **Renderer Dependency on VM** | **50%** | 100% | `render_markdown.py` uses the VM. `build.py` uses manual JSONs. |
| **Manual Data Sources** | **1** | 0 | `templates/cv/profiles/*.json` are still required to fill the gaps. |

---

## 5. Phase 2 Conclusions

> **Can the current `professional_profile_vm.json` satisfy every renderer?**
> **Answer: NO.**

The evidence proves that the current View Model is **not functionally complete**. It suffers from missing fields (Competencies), severe type mismatches (Dictionaries vs Strings), and architectural data loss (Geographic locations).

### Required Remediation (Before Migration)
Before proceeding to Phase 3 (Refactoring Generators), `scripts/build_view_models.py` must be significantly expanded. We must either:
1. Extend `professional_profile_vm.json` so it achieves 100% data coverage of the required rendering fields.
2. Introduce specialized View Models (e.g., `portfolio_vm.json`, `recruiter_vm.json`) if a single monolithic schema becomes too complex.

Phase 2 is now complete. We have proven mathematically that we cannot safely deprecate the manual JSON profiles yet.
