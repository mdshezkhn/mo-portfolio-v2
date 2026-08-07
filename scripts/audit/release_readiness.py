import os
import re
import json

def scan_release_readiness(inventory, base_dir):
    print("==================================================")
    print(" Phase 5: Release Readiness & Supply Chain Audit  ")
    print("==================================================")
    
    findings = []
    
    # Absolute path pattern (e.g. C:\Users\... or /Users/...)
    local_path_pattern = re.compile(r'(?:C:\\Users\\[a-zA-Z0-9_\-\s]+|/Users/[a-zA-Z0-9_\-\s]+)', re.IGNORECASE)
    
    for item in inventory["files"]:
        rel_path = item["rel_path"]
        ext = item["extension"]
        size = item["size_bytes"]
        
        # 1. Supply chain: Large binary check (> 5MB)
        if size > 5 * 1024 * 1024 and ext in [".zip", ".tar", ".gz", ".exe", ".bin", ".iso", ".mp4"]:
            findings.append({
                "category": "large_binary",
                "severity": "Medium",
                "file": rel_path,
                "detail": f"Large binary asset ({size / (1024*1024):.2f} MB) detected in repository",
                "remediation": "Store large binaries in external release asset hosting or Git LFS."
            })
            
        # 2. Executable permission check
        if item.get("is_executable", False) and ext not in [".sh", ".py", ".js", ".bat", ".ps1"]:
            findings.append({
                "category": "suspicious_executable",
                "severity": "High",
                "file": rel_path,
                "detail": f"Non-standard executable file detected ({ext})",
                "remediation": "Remove executable permissions or audit source of binary."
            })
            
        # 3. Content scan for local absolute path leaks in source/compiled files
        if size < 2 * 1024 * 1024 and ext in [".py", ".js", ".json", ".html", ".md", ".yml", ".yaml"]:
            abs_path = os.path.join(base_dir, rel_path)
            try:
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                matches = local_path_pattern.findall(content)
                if matches and "scripts/audit/" not in rel_path and "audit_results.json" not in rel_path:
                    # Filter out standard code comments if any
                    unique_paths = list(set(matches))[:3]
                    findings.append({
                        "category": "local_path_leak",
                        "severity": "Medium",
                        "file": rel_path,
                        "detail": f"Hardcoded absolute local path detected: {', '.join(unique_paths)}",
                        "remediation": "Use relative paths or environment variables (e.g. os.path.abspath(__file__))."
                    })
            except Exception:
                pass
                
    # 4. Dependency manifest presence check
    pkg_json = os.path.join(base_dir, "package.json")
    req_txt = os.path.join(base_dir, "requirements.txt")
    if not os.path.exists(pkg_json) and not os.path.exists(req_txt):
        findings.append({
            "category": "missing_manifest",
            "severity": "Low",
            "file": ".",
            "detail": "No standard dependency manifest (package.json / requirements.txt) found at root",
            "remediation": "Create dependency manifest to guarantee build reproducibility."
        })
        
    print(f"-> Release Readiness Audit completed. Found {len(findings)} items.")
    return findings
