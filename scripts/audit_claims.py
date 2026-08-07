import os
import yaml
import sys

def load_yaml(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def audit_claims():
    claims_file = 'career-data/facts/claims.yml'
    evidence_file = 'career-data/facts/evidence.yml'
    
    claims_data = load_yaml(claims_file)
    evidence_data = load_yaml(evidence_file)
    
    if not claims_data or not evidence_data:
        print("Cannot find claims.yml or evidence.yml for auditing.")
        sys.exit(1)
        
    claims = claims_data.get('claims', [])
    evidences = evidence_data.get('evidence', [])
    
    evidence_ids = {e['id'] for e in evidences if 'id' in e}
    claim_ids = set()
    
    errors = []
    
    for c in claims:
        cid = c.get('id')
        if not cid:
            continue
            
        if cid in claim_ids:
            errors.append(f"Duplicate claim ID found: {cid}")
        claim_ids.add(cid)
        
        c_evidence = c.get('evidence', [])
        for eid in c_evidence:
            if eid not in evidence_ids:
                errors.append(f"Claim {cid} references invalid or missing evidence: {eid}")
                
    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        return False
        
    print("[PASS] All claim cross-references to evidence are valid.")
    return True

if __name__ == '__main__':
    if not audit_claims():
        sys.exit(1)
