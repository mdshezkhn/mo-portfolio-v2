import os
import re
import json

PII_PATTERNS = [
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', "email_address"),
    (r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b', "phone_number"),
    (r'\b[A-Z][0-9]{8}\b', "passport_number"),
    (r'\b\d{3}-\d{2}-\d{4}\b', "national_id"),
]

def load_allowlist(base_dir):
    allowlist_path = os.path.join(base_dir, "governance", "privacy_allowlist.yaml")
    allowed = set()
    if os.path.exists(allowlist_path):
        try:
            with open(allowlist_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Simple extraction of entity strings from yaml
                matches = re.findall(r'entity:\s*"([^"]+)"', content)
                allowed.update(matches)
        except Exception:
            pass
    return allowed

def scan_pii(inventory, base_dir):
    print("==================================================")
    print(" Phase 2: Executing PII Exposure Audit           ")
    print("==================================================")
    
    allowlist = load_allowlist(base_dir)
    findings = []
    
    for item in inventory["files"]:
        rel_path = item["rel_path"]
        ext = item["extension"]
        
        if item["size_bytes"] < 2 * 1024 * 1024 and ext in [".py", ".js", ".json", ".md", ".yml", ".yaml", ".html", ".txt"]:
            abs_path = os.path.join(base_dir, rel_path)
            try:
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                for pattern, pii_type in PII_PATTERNS:
                    for m in re.finditer(pattern, content):
                        val = m.group(0)
                        
                        # Skip if in allowlist
                        if val in allowlist or any(al in val for al in allowlist):
                            status = "Informational"
                            desc = "Approved Public Attribute (In Allowlist)"
                        elif pii_type in ["passport_number", "national_id"]:
                            status = "Critical"
                            desc = f"Unintentional High-Risk PII Exposure ({pii_type})"
                        elif pii_type == "email_address" and ("example.com" in val or "test.com" in val):
                            status = "Informational"
                            desc = "Mock / Example Email Address"
                        elif pii_type == "email_address":
                            status = "High"
                            desc = "Unverified Email Exposure"
                        else:
                            status = "Medium"
                            desc = f"Potential Private PII Entity ({pii_type})"
                            
                        if status != "Informational":
                            findings.append({
                                "category": "pii_exposure",
                                "severity": status,
                                "file": rel_path,
                                "detail": f"{desc}: '{val}'",
                                "remediation": "Redact or add entity to privacy_allowlist.yaml if intentionally public."
                            })
            except Exception as e:
                pass
                
    print(f"-> PII Audit completed. Found {len(findings)} flagged items.")
    return findings
