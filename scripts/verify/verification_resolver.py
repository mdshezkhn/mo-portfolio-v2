import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
CAREER_DATA = BASE_DIR / "career-data"

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def resolve_verification_state():
    """
    Returns a dict with resolved statuses for EMP and CLAIM IDs.
    {
       'EMP-2003': {'status': 'VERIFIED', 'reason': '...'},
       'CLAIM-1003': {'status': 'UNVERIFIED', 'reason': '...'}
    }
    """
    edges_data = load_yaml(CAREER_DATA / "relationships" / "edges.yml").get("edges", [])
    emps_data = load_yaml(CAREER_DATA / "facts" / "employment.yml").get("employment_records", [])
    
    claims_path = CAREER_DATA / "facts" / "claims.yml"
    claims_data = load_yaml(claims_path).get("claims", []) if claims_path.exists() else []
    golden_claims_path = CAREER_DATA / "golden" / "E-001" / "source" / "facts" / "claims.yml"
    golden_claims_data = load_yaml(golden_claims_path).get("claims", []) if golden_claims_path.exists() else []
    
    all_claims = {c['id']: c for c in claims_data + golden_claims_data}
    all_emps = {e['id']: e for e in emps_data}
    
    ev_assertions_path = CAREER_DATA / "facts" / "evidence_assertions.yml"
    ev_assertions = load_yaml(ev_assertions_path).get("evidence_assertions", []) if ev_assertions_path.exists() else []
    all_ev = {ev['evidence_id']: ev for ev in ev_assertions}
    
    resolved = {}
    
    # 1. Resolve EMPs
    # An EMP is VERIFIED iff it possesses a valid evidence edge (SUPPORTED_BY E-*)
    for emp_id in all_emps.keys():
        evidence_edges = [e for e in edges_data if e['from'] == emp_id and e['type'] == 'SUPPORTED_BY' and e['to'].startswith('E-')]
        if evidence_edges:
            # We assume graph_validator already ran and confirmed it's not contradictory.
            resolved[emp_id] = {'status': 'VERIFIED', 'reason': 'Has valid evidence edge'}
        else:
            resolved[emp_id] = {'status': 'UNVERIFIED', 'reason': 'Missing employment evidence edge'}
            
    # 2. Resolve CLAIMs
    # A CLAIM is VERIFIED iff:
    # - it has a valid evidence edge
    # - referenced evidence exists
    # - evidence supports the claim
    # - it has a valid attribution relationship to an EMP
    # - that EMP is VERIFIED
    for claim_id, claim_data in all_claims.items():
        if claim_data.get('verification_status') == 'unresolved':
            resolved[claim_id] = {'status': 'UNVERIFIED', 'reason': claim_data.get('verification_reason', 'Unresolved in canonical data')}
            continue
            
        emp_edges = [e for e in edges_data if e['from'] == claim_id and e['type'] == 'SUPPORTED_BY' and e['to'].startswith('EMP-')]
        ev_edges = [e for e in edges_data if e['from'] == claim_id and e['type'] == 'SUPPORTED_BY' and e['to'].startswith('E-')]
        
        if not emp_edges:
            resolved[claim_id] = {'status': 'UNVERIFIED', 'reason': 'Missing edge to EMP'}
            continue
            
        if not ev_edges:
            resolved[claim_id] = {'status': 'UNVERIFIED', 'reason': 'Missing edge to Evidence'}
            continue
            
        emp_id = emp_edges[0]['to']
        ev_id = ev_edges[0]['to']
        
        if resolved.get(emp_id, {}).get('status') != 'VERIFIED':
            resolved[claim_id] = {'status': 'UNVERIFIED', 'reason': f'Parent EMP {emp_id} is UNVERIFIED'}
            continue
            
        if ev_id not in all_ev:
            resolved[claim_id] = {'status': 'UNVERIFIED', 'reason': f'Evidence {ev_id} does not exist'}
            continue
            
        # Check if evidence supports the claim
        supported_claims = all_ev[ev_id].get('assertions', {}).get('supported_claims', [])
        if claim_id not in supported_claims:
            resolved[claim_id] = {'status': 'UNVERIFIED', 'reason': f'Evidence {ev_id} does not assert support for {claim_id}'}
            continue
            
        resolved[claim_id] = {'status': 'VERIFIED', 'reason': 'Valid lineage'}
        
    return resolved

if __name__ == "__main__":
    import pprint
    pprint.pprint(resolve_verification_state())
