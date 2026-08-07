import os
import sys
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.audit.browser_detector import scan_browser_artifacts

def run_privacy_gate():
    print("====================================")
    print(" RC-7: Privacy Gate Execution      ")
    print("====================================")
    
    is_release_build = "--release" in sys.argv
    failed = False
    flagged_privacy_items = []
    
    for root, dirs, files in os.walk(BASE_DIR):
        if any(skip in root for skip in [".git", "node_modules", "quarantine", "__pycache__", ".playwright-mcp"]):
            continue
            
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), BASE_DIR).replace("\\", "/")
            
            if f in ["Login Data", "Cookies", "History", "Web Data", "cookies.sqlite", "logins.json", "key4.db"]:
                flagged_privacy_items.append(("High", rel, f"Browser artifact database file '{f}' detected"))
                
            if ".playwright" in rel.lower() or "user-data" in rel.lower():
                flagged_privacy_items.append(("High", rel, "Persistent browser profile directory file detected"))
                
    if not flagged_privacy_items:
        print("[PASS] RC-7 Privacy Gate passed cleanly (0 privacy violations).\n")
        return 0
        
    for sev, path, msg in flagged_privacy_items:
        print(f"[{sev}] {msg} at `{path}`")
        if sev in ["Critical", "High"] or (sev == "Medium" and is_release_build):
            failed = True
            
    if failed:
        print("\n[FAIL] RC-7 Privacy Gate FAILED due to unhandled high-severity privacy artifacts.")
        return 1
    else:
        print("\n[WARN] RC-7 Privacy Gate passed with local development warnings.\n")
        return 0

if __name__ == "__main__":
    sys.exit(run_privacy_gate())
