import os
import sys
import json
import hashlib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GOVERNANCE_DIR = os.path.join(BASE_DIR, "governance")
MANIFEST_FILE = os.path.join(GOVERNANCE_DIR, "governance_manifest.json")

POLICY_FILES = [
    "privacy_policy.yaml",
    "privacy_allowlist.yaml",
    "security_baseline.json"
]

def calculate_sha256(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def run_governance_gate():
    print("====================================")
    print(" RC-10: Governance Integrity Gate Execution")
    print("====================================")
    
    update_manifest = "--update-manifest" in sys.argv
    current_hashes = {}
    
    for pf in POLICY_FILES:
        path = os.path.join(GOVERNANCE_DIR, pf)
        if not os.path.exists(path):
            print(f"[FAIL] Required governance policy file '{pf}' missing at `{path}`")
            return 1
        current_hashes[pf] = calculate_sha256(path)
        
    if update_manifest or not os.path.exists(MANIFEST_FILE):
        manifest_data = {
            "version": "1.0.0",
            "policy_hashes": current_hashes
        }
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)
        print(f"[PASS] Updated governance integrity manifest at `{MANIFEST_FILE}`.\n")
        return 0
        
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
        
    recorded_hashes = manifest_data.get("policy_hashes", {})
    mutations = []
    
    for pf, cur_h in current_hashes.items():
        rec_h = recorded_hashes.get(pf)
        if cur_h != rec_h:
            mutations.append((pf, rec_h, cur_h))
            
    if mutations:
        print("[FAIL] RC-10 Governance Integrity Gate FAILED: Unapproved policy mutation detected!")
        for pf, old_h, new_h in mutations:
            print(f"  - Policy file '{pf}' modified without manifest sign-off!")
            print(f"    Expected hash: {old_h}")
            print(f"    Observed hash: {new_h}")
        print("\nRun `python scripts/verify/governance_gate.py --update-manifest` after reviewing policy changes.")
        return 1
        
    print("[PASS] RC-10 Governance Integrity Gate passed cleanly (0 unapproved policy mutations).\n")
    return 0

if __name__ == "__main__":
    sys.exit(run_governance_gate())
