# Migration from Legacy String Renderers to Canonical Graph Pipeline (v1 to v2)

This document serves as an immutable historical record of the architectural changes made during the `v2.0.0` migration. 

## Architectural Rationale

The original `v1` architecture relied heavily on a monolithic procedural builder and `master.json` fallback templates. As the underlying canonical career data grew more complex, the `v1` architecture could no longer guarantee data purity, often duplicating or overriding canonical facts with legacy strings.

The `v2` architecture solves this by separating concerns into a strict pipeline:
`Canonical YAML Facts -> Resolved Graph -> Domain Model -> Projection Contracts -> View Models -> Renderers`

## Regression Contract Change: Byte-for-Byte to Structural Equivalence

During the migration, it became necessary to redefine the meaning of our regression tests.

Initially, the legacy regression tests strictly enforced **byte-for-byte equivalence** (`text_legacy == text_v2`). This was appropriate when only the renderer was changing but the underlying data was frozen. 

However, since the `v2` migration also involved replacing the legacy generator and updating the Domain Model to draw purely from the canonical graph, enforcing byte-for-byte equality blocked valid improvements in the canonical data (e.g., removing outdated claims). 

Therefore, the regression test contract has been formally changed to **Level 1 Structural Equivalence**. The tests now prove that *"the new system contains the same information structure"* rather than *"the exact same text behaviour."*

### Regression Equivalence Levels

To prevent future maintainers from misunderstanding what "regression" actually means, we have defined three strict levels of equivalence:

| Level   | Meaning              | Used For          |
| ------- | -------------------- | ----------------- |
| Level 0 | Byte identical       | Migration scaffolding only |
| Level 1 | Structural identical | Permanent CI Gates |
| Level 2 | Semantic identical   | Domain validation |

### Formal Definition of Structural Equivalence

Structural equivalence means:
* Identical section inventory
* Identical ordering
* Identical entity count
* Identical entity identifiers
* Identical evidence identifiers
* Identical chronology
* Identical semantic relationships

Whitespace, typography, punctuation, date formatting, and wording are intentionally ignored.

## Removed Components

The following legacy components have been permanently retired:
* `scripts/build_view_models.py`
* `scripts/render_markdown.py`
* `templates/cv/profiles/`

## Future Migrations

This file is an immutable historical record of the `v1` to `v2` transition. Any future architectural changes (e.g., to `v3`) must be documented in a new file, such as `MIGRATION_V2_TO_V3.md`.

## Future Recommendations
* **Dependency Lockfiles:** For future major releases (e.g., `v3`), it is highly recommended to migrate from pinned `requirements.txt` to a strict lockfile mechanism (like `uv lock`, `pip-tools`, or `Poetry lock`) to guarantee absolute environment reproducibility across CI pipelines.
