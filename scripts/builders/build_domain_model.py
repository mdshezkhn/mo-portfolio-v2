import json
import yaml
from pathlib import Path
import sys
import shutil

BASE_DIR = Path(__file__).parent.parent.parent
CAREER_DATA = BASE_DIR / "career-data"
ARTIFACTS_DIR = BASE_DIR / "artifacts" / "cv_view_models"
POLICIES_PATH = BASE_DIR / "governance" / "cv_policies.yml"

# Import validator and resolver
sys.path.append(str(BASE_DIR))
from scripts.verify.graph_validator import validate_graph
from scripts.verify.verification_resolver import resolve_verification_state

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def build():
    # 1. Clear Artifacts
    if ARTIFACTS_DIR.exists():
        shutil.rmtree(ARTIFACTS_DIR)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 2. Graph Validation (Fails build if corrupt)
    validate_graph()
    
    # 3. Verification Resolver
    resolved_states = resolve_verification_state()
    
    # Load canonical data
    emps = load_yaml(CAREER_DATA / "facts" / "employment.yml").get('employment_records', [])
    claims_path = CAREER_DATA / "facts" / "claims.yml"
    claims_data = load_yaml(claims_path).get("claims", []) if claims_path.exists() else []
    golden_claims_path = CAREER_DATA / "golden" / "E-001" / "source" / "facts" / "claims.yml"
    golden_claims_data = load_yaml(golden_claims_path).get("claims", []) if golden_claims_path.exists() else []
    all_claims = {c['id']: c for c in claims_data + golden_claims_data}
    
    policies_doc = load_yaml(POLICIES_PATH)
    policies = policies_doc.get('policies', {})
    verification_rules = policies_doc.get('verification_rules', {})
    
    # Load identity, summary etc from graph if needed, for simplicity we just load minimal CV fields
    # Here I'll mock the identity/summary just to keep the build working
    identity = {"name": "Mohammed Shehzad Khan"}
    
    # Load canonical dictionaries for name resolution
    orgs = {o['id']: o['canonical_name'] for o in load_yaml(CAREER_DATA / "facts" / "organisations.yml").get('organisations', [])}
    roles = {r['id']: r['title'] for r in load_yaml(CAREER_DATA / "facts" / "roles.yml").get('roles', [])}
    insts = {i['id']: i['canonical_name'] for i in load_yaml(CAREER_DATA / "facts" / "institutions.yml").get('institutions', [])}
    
    # 4. Policy Engine & View Model Generation
    for policy_name, policy_conf in policies.items():
        if policy_conf.get('active', True) is False:
            print(f"Skipping inactive policy {policy_name}...")
            continue
            
        print(f"Building View Model for {policy_name}...")
        
        # Policy rules
        policy_rules = verification_rules.get(policy_name, verification_rules.get('master', {}))
        approved_emp_statuses = policy_rules.get('employment', {}).get('approved_statuses', ['approved'])
        
        view_model = {
            "title": policy_conf.get('title', policy_name.capitalize()),
            "experience": []
        }
        
        # We sort emps by date
        sorted_emps = sorted(emps, key=lambda e: e.get('dates', {}).get('start', ''), reverse=True)
        
        for emp in sorted_emps:
            emp_id = emp['id']
            
            # Policy Rule 1: Canonical review_status must be in approved list
            if emp.get('review_status', 'pending') not in approved_emp_statuses:
                continue
                
            # Build presentation entry
            org_id = emp.get('employer_id', 'Unknown')
            role_id = emp.get('role_id', 'Unknown')
            org_name = orgs.get(org_id, org_id)
            role_name = roles.get(role_id, role_id)
            start = emp.get('dates', {}).get('start', '')
            end = emp.get('dates', {}).get('end', 'Present')
            
            exp_entry = {
                "id": emp_id,
                "company": org_name,
                "role": role_name,
                "date": f"{start} - {end}",
                "bullets": []
            }
            
            # Policy Rule 3: Only VERIFIED canonical claims enter presentation
            for highlight in emp.get('cv_highlights', []):
                # Historical strings are excluded automatically because they don't have claim_ids.
                if isinstance(highlight, dict) and 'claim_id' in highlight:
                    claim_id = highlight['claim_id']
                    claim_resolved = resolved_states.get(claim_id, {})
                    
                    if claim_resolved.get('status') == 'VERIFIED':
                        claim_text = all_claims.get(claim_id, {}).get('statement', '')
                        exp_entry["bullets"].append(claim_text)
            
            view_model['experience'].append(exp_entry)
            
        # Education / Qualifications
        view_model['qualifications'] = []
        all_quals = load_yaml(CAREER_DATA / "facts" / "education.yml").get('education_records', [])
        for qual in all_quals:
            qual_id = qual['id']
            if resolved_states.get(qual_id, {}).get('status') == 'VERIFIED':
                inst_id = qual.get("institution_id")
                inst_name = insts.get(inst_id, inst_id)
                start = qual.get("dates", {}).get("start", "")
                end = qual.get("dates", {}).get("end", "")
                view_model['qualifications'].append({
                    "id": qual_id,
                    "degree": qual.get("degree"),
                    "institution": inst_name,
                    "date": f"{start} - {end}" if start and end else (end or start),
                    "entity_type": qual.get("entity_type", "qualification")
                })
            
        out_filename = f"{policy_name}.json"
        out_filepath = ARTIFACTS_DIR / out_filename
        with open(out_filepath, "w", encoding="utf-8", newline='\n') as f:
            json.dump(view_model, f, indent=2)
            
    print("Done building view models.")

if __name__ == "__main__":
    build()
