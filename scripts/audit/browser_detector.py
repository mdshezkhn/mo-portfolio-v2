import os
import json

BROWSER_FILE_PATTERNS = {
    "Login Data": ("Chromium Login Credentials Database", "High"),
    "Cookies": ("Chromium Session Cookies Database", "High"),
    "History": ("Chromium Browsing History Database", "High"),
    "Web Data": ("Chromium Web Data & Autofill Database", "High"),
    "cookies.sqlite": ("Firefox Session Cookies SQLite DB", "High"),
    "places.sqlite": ("Firefox History/Bookmarks SQLite DB", "High"),
    "logins.json": ("Firefox Saved Logins JSON", "High"),
    "key4.db": ("Firefox Password Master Key DB", "Critical"),
    "storage.json": ("Playwright/Puppeteer Saved State Storage", "High"),
    "state.json": ("Browser Persistent Context State", "High")
}

KNOWN_BROWSER_TABLES = [
    b"logins", b"cookies", b"meta", b"urls", b"autofill", 
    b"moz_cookies", b"moz_places", b"web_app_settings", b"http_auth"
]

def is_structural_browser_sqlite(filepath):
    """
    Inspects file header and byte structure to detect SQLite browser databases
    regardless of filename (e.g. even if Login Data is renamed to data.db).
    """
    try:
        with open(filepath, "rb") as f:
            header = f.read(100)
            if not header.startswith(b"SQLite format 3\x00"):
                return False, None
                
            # Read first 100KB to inspect table schema names
            f.seek(0)
            chunk = f.read(100000)
            
            matched_tables = [table.decode("ascii") for table in KNOWN_BROWSER_TABLES if table in chunk]
            if len(matched_tables) >= 1:
                return True, f"SQLite Browser DB (tables: {', '.join(matched_tables)})"
    except Exception:
        pass
    return False, None

def scan_browser_artifacts(inventory_files, base_dir):
    findings = []
    
    for item in inventory_files:
        rel_path = item["rel_path"]
        filename = item["filename"]
        abs_path = os.path.join(base_dir, rel_path)
        
        # 1. Filename match
        if filename in BROWSER_FILE_PATTERNS:
            desc, severity = BROWSER_FILE_PATTERNS[filename]
            findings.append({
                "category": "browser_artifact",
                "severity": severity,
                "file": rel_path,
                "detail": f"Detected {desc} ({filename})",
                "remediation": "Move artifact to quarantine and exclude directory in .gitignore."
            })
            continue
            
        # 2. Directory match
        if ".playwright" in rel_path.lower() or "user-data" in rel_path.lower() or "chrome-data" in rel_path.lower():
            findings.append({
                "category": "browser_profile_directory",
                "severity": "High",
                "file": rel_path,
                "detail": "File located inside persistent browser profile / automation directory",
                "remediation": "Quarantine browser profile directory and add rule to .gitignore."
            })
            continue
            
        # 3. Structural SQLite Match (handles renamed browser databases like data.db)
        if item["size_bytes"] > 0 and item["size_bytes"] < 50 * 1024 * 1024:
            is_browser_db, desc = is_structural_browser_sqlite(abs_path)
            if is_browser_db:
                findings.append({
                    "category": "browser_artifact_renamed",
                    "severity": "High",
                    "file": rel_path,
                    "detail": f"Structurally identified renamed browser database: {desc}",
                    "remediation": "Move renamed database file to quarantine."
                })
            
    return findings
