import os
import re
import json
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.audit.browser_detector import scan_browser_artifacts

SECRET_PATTERNS = [
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token", "Critical"),
    (r'gho_[a-zA-Z0-9]{36}', "GitHub OAuth Access Token", "Critical"),
    (r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}', "GitHub Fine-Grained Personal Access Token", "Critical"),
    (r'sk-ant-api[a-zA-Z0-9_\-]{40,}', "Anthropic API Key", "Critical"),
    (r'sk-[a-zA-Z0-9]{32,}', "OpenAI API Key", "Critical"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID", "Critical"),
    (r'AIzaSy[a-zA-Z0-9_\-]{33}', "Google API / Firebase Key", "Critical"),
    (r'xox[b|p|a|r]-[a-zA-Z0-9]{10,}', "Slack API Token", "Critical"),
    (r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}', "JSON Web Token (JWT)", "High"),
    (r'-----BEGIN (RSA|EC|OPENSSH|DSA|PRIVATE) KEY-----', "Private SSH/Crypto Key", "Critical"),
    (r'postgres://[a-zA-Z0-9_]+:[^@\s]+@', "PostgreSQL Connection String with Password", "Critical"),
    (r'mongodb(\+srv)?://[a-zA-Z0-9_]+:[^@\s]+@', "MongoDB Connection String with Password", "Critical"),
]

SENSITIVE_EXTENSIONS = {
    ".pem": ("PEM Private Certificate", "Critical"),
    ".p12": ("PKCS#12 Key Store", "Critical"),
    ".pfx": ("PFX Key Store", "Critical"),
    ".ovpn": ("OpenVPN Configuration File", "High"),
    ".key": ("Private Key File", "Critical"),
    ".swp": ("Vim Swap File", "Low"),
    ".swo": ("Vim Swap File", "Low"),
}

def scan_security(inventory, base_dir):
    print("==================================================")
    print(" Phase 1: Executing Repository Security Audit    ")
    print("==================================================")
    
    findings = []
    
    # 1. Run browser detector (including structural SQLite detection)
    browser_findings = scan_browser_artifacts(inventory["files"], base_dir)
    findings.extend(browser_findings)
    
    # 2. File name and extension checks
    for item in inventory["files"]:
        rel_path = item["rel_path"]
        ext = item["extension"]
        filename = item["filename"]
        
        if filename.startswith(".env"):
            findings.append({
                "category": "environment_file",
                "severity": "Critical",
                "file": rel_path,
                "detail": f"Environment configuration file detected ({filename})",
                "remediation": "Remove or quarantine file and ensure .env is listed in .gitignore."
            })
            
        if ext in SENSITIVE_EXTENSIONS:
            desc, severity = SENSITIVE_EXTENSIONS[ext]
            findings.append({
                "category": "sensitive_extension",
                "severity": severity,
                "file": rel_path,
                "detail": f"Detected sensitive file extension: {desc}",
                "remediation": "Verify necessity, move to quarantine if unapproved."
            })
            
        # 3. Content scanning for text/code files
        if item["size_bytes"] < 5 * 1024 * 1024 and ext in [".py", ".js", ".json", ".md", ".yml", ".yaml", ".html", ".txt", ".sh", ".bat", ".ps1"]:
            abs_path = os.path.join(base_dir, rel_path)
            try:
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                for pattern, desc, severity in SECRET_PATTERNS:
                    matches = re.finditer(pattern, content)
                    for m in matches:
                        snippet = content[max(0, m.start()-15):min(len(content), m.end()+15)]
                        findings.append({
                            "category": "secret_leak",
                            "severity": severity,
                            "file": rel_path,
                            "detail": f"Detected {desc}: '{snippet.strip()}'",
                            "remediation": "Revoke secret immediately, remove key from file, and rewrite history if committed."
                        })
            except Exception:
                pass

    print(f"-> Security Audit completed. Found {len(findings)} items.")
    return findings
