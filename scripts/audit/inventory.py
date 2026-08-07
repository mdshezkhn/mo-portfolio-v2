import os
import json
import hashlib
import sys
from datetime import datetime

SCHEMA_VERSION = "1.0.0"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIT_DIR = os.path.join(BASE_DIR, "audit")
OUTPUT_FILE = os.path.join(AUDIT_DIR, "REPOSITORY_INVENTORY.json")

# Directories to skip traversing
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", "venv", ".venv"}

def calculate_sha256(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def is_ignored(rel_path):
    # Simple check for common ignored folders/patterns
    parts = rel_path.split(os.sep)
    if any(p in {".claude", ".playwright-mcp", "node_modules", "temp_certs", "quarantine"} for p in parts):
        return True
    return False

def generate_inventory():
    print("==================================================")
    print(" Phase 0: Generating Repository File Inventory   ")
    print("==================================================")
    
    if not os.path.exists(AUDIT_DIR):
        os.makedirs(AUDIT_DIR)
        
    inventory = []
    total_files = 0
    total_bytes = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        # Filter out directories to skip
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, BASE_DIR)
            
            try:
                stat = os.stat(abs_path)
                size_bytes = stat.st_size
                ext = os.path.splitext(file)[1].lower()
                sha256 = calculate_sha256(abs_path)
                ignored = is_ignored(rel_path)
                
                item = {
                    "rel_path": rel_path.replace("\\", "/"),
                    "filename": file,
                    "extension": ext,
                    "size_bytes": size_bytes,
                    "sha256": sha256,
                    "ignored": ignored,
                    "is_executable": os.access(abs_path, os.X_OK) and ext in [".exe", ".bat", ".cmd", ".sh", ".ps1"]
                }
                inventory.append(item)
                total_files += 1
                total_bytes += size_bytes
            except Exception as e:
                print(f"Warning: Could not inventory {rel_path}: {e}")
                
    result = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now().isoformat(),
        "repository_root": BASE_DIR,
        "summary": {
            "total_files": total_files,
            "total_size_bytes": total_bytes
        },
        "files": inventory
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print(f"-> Inventory successfully generated with {total_files} files ({total_bytes} bytes).")
    print(f"-> Output saved to: {OUTPUT_FILE}\n")
    return result

if __name__ == "__main__":
    generate_inventory()
