import os
import yaml
import sys

def load_yaml(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def audit_evidence():
    claims_file = 'career-data/facts/claims.yml'
    evidence_file = 'career-data/facts/evidence.yml'
    
    claims_data = load_yaml(claims_file)
    evidence_data = load_yaml(evidence_file)
    
    if not claims_data or not evidence_data:
        print("Cannot find claims.yml or evidence.yml for auditing.")
        sys.exit(1)
        
    claims = claims_data.get('claims', [])
    evidences = evidence_data.get('evidence', [])
    
    # Collect all used evidence IDs in claims
    used_evidence_ids = set()
    for c in claims:
        used_evidence_ids.update(c.get('evidence', []))
        
    evidence_ids = set()
    errors = []
    
    for e in evidences:
        eid = e.get('id')
        if not eid:
            continue
            
        if eid in evidence_ids:
            errors.append(f"Duplicate evidence ID found: {eid}")
        evidence_ids.add(eid)
        
        if eid not in used_evidence_ids:
            errors.append(f"Orphan evidence found: {eid} is not referenced by any claim.")
            
    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        return False
        
    print("[PASS] All evidence items are referenced and unique.")
    return True

if __name__ == '__main__':
    if not audit_evidence():
        sys.exit(1)
