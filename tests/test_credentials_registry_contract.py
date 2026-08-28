"""
Credentials Registry Contract Test
==================================

Ensures the in-browser credentials registry (mo-portfolio-v2/assets/js/credentials-registry.js)
stays aligned with the canonical ID registry (registry/ids.yml) and the
public-CV projection in artifacts/cv_view_models/portfolio.json.

Three invariants are checked:

1. No two registry entries may share the same `canonical_id` (duplicates).
2. Every public registry entry's `canonical_id` must exist in registry/ids.yml.
3. Every canonical education/certification ID flagged "published" in
   registry/ids.yml and exposed in the public portfolio view model must have
   a corresponding registry entry (so the modal actually opens).

The test is intentionally read-only — it inspects the source files but does
not modify them. Run with: python -m pytest tests/test_credentials_registry_contract.py
"""
import json
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "registry" / "ids.yml"
JS_REGISTRY_PATH = ROOT / "mo-portfolio-v2" / "assets" / "js" / "credentials-registry.js"
PORTFOLIO_VM_PATH = ROOT / "artifacts" / "cv_view_models" / "portfolio.json"


def _parse_canonical_ids_from_js():
    """Extract the literal `canonical_id` and `id` values from the JS source.

    We do a simple regex parse because the file is small and the format is
    stable — no JS evaluation needed. The block we read sits inside
    CREDENTIALS_REGISTRY = [ { ... }, ... ]; each entry may declare
    `canonical_id: "QUAL-XXXX"` and an optional `id: "..."` legacy alias.
    """
    text = JS_REGISTRY_PATH.read_text(encoding="utf-8")
    # Slice from the first `[` after CREDENTIALS_REGISTRY to the matching `];`
    match = re.search(r"CREDENTIALS_REGISTRY\s*=\s*\[(.*?)\n\];", text, re.DOTALL)
    assert match, "Could not locate CREDENTIALS_REGISTRY block in JS source"
    block = match.group(1)

    entries = []
    for entry_match in re.finditer(r"\{(.*?)\n\s*\},", block, re.DOTALL):
        entry_body = entry_match.group(1)
        canonical = re.search(r'canonical_id\s*:\s*"([^"]+)"', entry_body)
        legacy_id = re.search(r'^\s*id\s*:\s*"([^"]+)"', entry_body, re.MULTILINE)
        if not canonical:
            continue
        entries.append({
            "canonical_id": canonical.group(1),
            "legacy_id": legacy_id.group(1) if legacy_id else None,
        })
    return entries


def test_no_duplicate_canonical_ids():
    """Two registry entries must not share the same canonical_id."""
    entries = _parse_canonical_ids_from_js()
    seen = {}
    duplicates = []
    for e in entries:
        if e["canonical_id"] in seen:
            duplicates.append(e["canonical_id"])
        seen[e["canonical_id"]] = True
    assert not duplicates, f"Duplicate canonical_id in registry: {duplicates}"


def test_every_canonical_id_is_registered():
    """Every registry canonical_id must exist in registry/ids.yml."""
    entries = _parse_canonical_ids_from_js()
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    known = set(registry.get("entities", {}).keys())

    missing = [e["canonical_id"] for e in entries if e["canonical_id"] not in known]
    assert not missing, (
        f"Registry entries reference canonical_ids not in registry/ids.yml: {missing}"
    )


def test_public_credentials_have_registry_entry():
    """Every public qualification in the portfolio view model must be in the registry.

    This is the "UI metadata ↔ canonical credential" half of the contract.
    """
    if not PORTFOLIO_VM_PATH.exists():
        pytest.skip(f"Portfolio view model not found: {PORTFOLIO_VM_PATH}")

    vm = json.loads(PORTFOLIO_VM_PATH.read_text(encoding="utf-8"))
    public_qual_ids = {
        q["id"] for q in vm.get("qualifications", [])
        if q.get("entity_type") in ("qualification", "certification")
    }

    entries = _parse_canonical_ids_from_js()
    registered_ids = {e["canonical_id"] for e in entries}

    # Only check qualifications that look like canonical IDs (QUAL-XXXX).
    # Education-only items like 'institution' are not registry entries.
    missing = sorted(
        qid for qid in public_qual_ids
        if qid.startswith("QUAL-") and qid not in registered_ids
    )
    assert not missing, (
        f"Public qualifications have no UI metadata in credentials-registry.js: {missing}"
    )


def test_matching_logic_uses_canonical_id():
    """The matchById function must compare canonical_id (lowercased) to data-cert-id.

    Guards against future regressions that re-introduce the legacy `id` field
    as the primary match key.
    """
    text = JS_REGISTRY_PATH.read_text(encoding="utf-8")
    assert "item.canonical_id" in text, (
        "renderCredentialsRegistry() must reference item.canonical_id when matching cards"
    )
    assert "toLowerCase()" in text, (
        "renderCredentialsRegistry() must lowercase the canonical_id to match the DOM projection"
    )
