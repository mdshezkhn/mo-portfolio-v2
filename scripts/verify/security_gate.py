import os
import sys
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

SECRET_PATTERNS = [
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
    (r'sk-ant-api[a-zA-Z0-9_\-]{40,}', "Anthropic API Key"),
    (r'sk-[a-zA-Z0-9]{32,}', "OpenAI API Key"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
    (r'-----BEGIN (RSA|EC|OPENSSH|DSA|PRIVATE) KEY-----', "Private SSH/Crypto Key")
]

def run_security_gate():
    print("====================================")
    print(" RC-8: Security Gate Execution     ")
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
            
            if f.startswith(".env") and f != ".env.example":
                flagged.append(("Critical", rel, f"Environment file '{f}' detected"))
                
            if ext in [".pem", ".p12", ".pfx", ".key"]:
                flagged.append(("Critical", rel, f"Private credential key store '{f}' detected"))
                
            if ext in [".py", ".js", ".json", ".yml", ".yaml", ".sh", ".bat", ".ps1"]:
                abs_p = os.path.join(root, f)
                try:
                    with open(abs_p, "r", encoding="utf-8", errors="ignore") as file_obj:
                        text = file_obj.read()
                    for pat, desc in SECRET_PATTERNS:
                        if re.search(pat, text):
                            flagged.append(("Critical", rel, f"Secret pattern '{desc}' detected"))
                except Exception:
                    pass
                    
    if not flagged:
        print("[PASS] RC-8 Security Gate passed cleanly (0 security vulnerabilities).\n")
        return 0
        
    for sev, path, msg in flagged:
        print(f"[{sev}] {msg} at `{path}`")
        if sev in ["Critical", "High"] or (sev == "Medium" and is_release_build):
            failed = True
            
    if failed:
        print("\n[FAIL] RC-8 Security Gate FAILED due to unhandled security secrets or keys.")
        return 1
    else:
        print("\n[WARN] RC-8 Security Gate passed with local development warnings.\n")
        return 0

if __name__ == "__main__":
    sys.exit(run_security_gate())
