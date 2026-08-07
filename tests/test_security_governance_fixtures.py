import os
import sys
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.audit.browser_detector import is_structural_browser_sqlite, scan_browser_artifacts
from scripts.audit.security import scan_security

FIXTURE_DIR = BASE_DIR / "tests" / "security_fixtures"

def test_renamed_sqlite_browser_database_fixture():
    """Verify that renamed SQLite browser databases are structurally flagged."""
    db_file = FIXTURE_DIR / "bad" / "renamed_sqlite.db"
    assert db_file.exists(), f"Fixture missing: {db_file}"
    is_detected, desc = is_structural_browser_sqlite(str(db_file))
    assert is_detected, f"Failed to structurally detect renamed SQLite database: {desc}"

def test_synthetic_bad_fixtures_detected():
    """Verify that synthetic secrets in the bad fixture corpus are detected."""
    bad_dir = FIXTURE_DIR / "bad"
    inventory = {
        "files": []
    }
    for item in bad_dir.iterdir():
        rel = str(item.relative_to(BASE_DIR)).replace("\\", "/")
        inventory["files"].append({
            "rel_path": rel,
            "filename": item.name,
            "extension": item.suffix,
            "size_bytes": item.stat().st_size
        })
        
    findings = scan_security(inventory, str(BASE_DIR))
    assert len(findings) >= 3, f"Expected at least 3 findings in bad fixture corpus, found {len(findings)}"

def test_clean_good_fixtures_pass():
    """Verify that clean fixtures produce zero security leaks."""
    good_file = FIXTURE_DIR / "good" / "clean_sample.txt"
    rel = str(good_file.relative_to(BASE_DIR)).replace("\\", "/")
    inventory = {
        "files": [
            {"rel_path": rel, "filename": good_file.name, "extension": good_file.suffix, "size_bytes": good_file.stat().st_size}
        ]
    }
    findings = scan_security(inventory, str(BASE_DIR))
    # Standard email in allowlist or clean content should produce zero secret leaks
    secrets = [f for f in findings if f.get("category") == "secret_leak"]
    assert len(secrets) == 0, f"Expected 0 secret leaks in clean fixture, found {len(secrets)}"
