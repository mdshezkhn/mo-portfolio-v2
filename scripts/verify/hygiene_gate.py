import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

FORBIDDEN_HYGIENE_EXTENSIONS = {".zip", ".tar", ".gz", ".rar", ".7z", ".iso", ".psd", ".tmp", ".bak"}

def run_hygiene_gate():
    print("====================================")
    print(" RC-9: Repository Hygiene Gate Execution")
    print("====================================")
    
    is_release_build = "--release" in sys.argv
    failed = False
    flagged = []
    
    for root, dirs, files in os.walk(BASE_DIR):
        if any(skip in root for skip in [".git", "node_modules", "quarantine", "__pycache__"]):
            continue
            
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), BASE_DIR).replace("\\", "/")
            ext = os.path.splitext(f)[1].lower()
            abs_p = os.path.join(root, f)
            size_bytes = os.path.getsize(abs_p)
            
            # 1. Archives and temporary formats (allow release-artifact.zip and Claude Code skills directory)
            if ext in FORBIDDEN_HYGIENE_EXTENSIONS:
                if rel != "release-artifact.zip" and "Claude Code skills" not in rel:
                    flagged.append(("High", rel, f"Unwanted archive/temporary format '{ext}' detected"))
                
            # 2. Large unapproved binaries (>5MB)
            if size_bytes > 5 * 1024 * 1024 and ext in [".bin", ".exe", ".iso", ".mp4"]:
                flagged.append(("Medium", rel, f"Large unapproved binary asset ({size_bytes / (1024*1024):.2f} MB) detected"))
                
            # 3. Temporary screenshots in root/draft folders
            if "screenshot" in f.lower() or "qa_shot" in f.lower() or "tmp_" in f.lower():
                if "compiled_assets" not in rel and "public_portfolio" not in rel:
                    flagged.append(("Low", rel, f"Stray temporary screenshot or artifact file '{f}' detected"))
                    
    if not flagged:
        print("[PASS] RC-9 Repository Hygiene Gate passed cleanly (0 hygiene issues).\n")
        return 0
        
    for sev, path, msg in flagged:
        print(f"[{sev}] {msg} at `{path}`")
        if sev in ["Critical", "High"] or (sev == "Medium" and is_release_build):
            failed = True
            
    if failed:
        print("\n[FAIL] RC-9 Repository Hygiene Gate FAILED due to unhandled repository clutter.")
        return 1
    else:
        print("\n[PASS] RC-9 Repository Hygiene Gate passed with minor warnings.\n")
        return 0

if __name__ == "__main__":
    sys.exit(run_hygiene_gate())
