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
from scripts.query_engine import load_graph

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def build_profile_domain_model(graph):
    # Retrieve base identities
    identity = list(graph.all().by_type('identity'))
    identity = identity[0] if identity else graph.entities_by_id.get('PERSON-1000', {})
    
    # Core domain entities
    employments = list(graph.employments())
    # Sort employments by start date newest first as a semantic invariant
    employments = sorted(employments, key=lambda e: e.get('dates', {}).get('start', ''), reverse=True)
    
    qualifications = list(graph.qualifications())
    
    claims = list(graph.claims())
    competencies = list(graph.all().by_type('competencie'))  # entity_type = 'competencie' due to rstrip('s') in resolve_graph.py
    
    master_path = BASE_DIR / "templates" / "cv" / "profiles" / "master.json"
    master_data = {}
    if master_path.exists():
        with open(master_path, "r", encoding="utf-8") as f:
            master_data = json.load(f)

    domain = {
        "candidate": {
            "name": identity.get("name", "Unknown Name"),
            "primary_title": master_data.get("title", identity.get("title")),
            "subtitle": identity.get("title", "").replace("International Primary Educator & EAL Specialist", "Primary Educator & EAL Specialist"),
            "summary": identity.get("summary", "").strip(),
            "contact_info": {}
        },
        "claims": [],
        "employment": [],
        "education": [],
        "competencies": []
    }
    
    # Map Claims
    for c in claims:
        stmt = c.get('statement')
        if not stmt:
            stmt = c.get('title', "Unknown Claim")
        domain["claims"].append({
            "id": c.get('id'),
            "statement": stmt,
            "priority": c.get('priority', 'low'),
            "tags": c.get('tags', [])
        })
        
    # Map Employments
    for emp in employments:
        emp_id = emp['id']
        
        # Org Name
        org_name = "Unknown Org"
        for edge in graph.edges:
            if edge.get('type') == 'WORKED_AT' and edge.get('from') == emp_id:
                org_entity = graph.entities_by_id.get(edge.get('to'))
                if org_entity:
                    org_name = org_entity.get('canonical_name', org_name)
                    
        # Role Title
        role_name = "Unknown Role"
        for edge in graph.edges:
            if edge.get('type') == 'HAS_ROLE' and edge.get('from') == emp_id:
                role_entity = graph.entities_by_id.get(edge.get('to'))
                if role_entity:
                    role_name = role_entity.get('title', role_name)
                    
        # Claims Supported
        supported_claims = []
        for edge in graph.edges:
            if edge.get('type') == 'SUPPORTED_BY' and edge.get('to') == emp_id:
                supported_claims.append(edge.get('from'))
                
        dates_block = emp.get('dates', {})
        start_val = dates_block.get('start', '')
        end_val = dates_block.get('end', '')
        
        # Evidence & Metadata
        evidence_id = None
        for edge in graph.edges:
            if edge.get('type') == 'EVIDENCED_BY' and edge.get('from') == emp_id:
                evidence_id = edge.get('to')
                break
        
        domain["employment"].append({
            "id": emp_id,
            "employer_name": org_name,
            "role_title": role_name,
            "master_date": None,
            "dates": {
                "start_date": start_val,
                "end_date": end_val,
                "is_present": not bool(end_val)
            },
            "location": {
                "physical_country": emp.get('physical_country'),
                "operational_regions": emp.get('operational_regions', [])
            },
            "supported_claims": supported_claims,
            "metadata": {
                "confidence": emp.get('confidence', 'unverified'),
                "evidence_id": evidence_id,
                "review_status": emp.get('review_status', 'pending')
            },
            "cv_highlights": emp.get('cv_highlights', [])
        })
        
    # Map Education
    for qual in qualifications:
        qual_id = qual['id']
        degree = qual.get('degree', 'Unknown Qualification')
        
        inst_name = "Unknown Institution"
        for edge in graph.edges:
            if edge.get('type') == 'STUDIED_AT' and edge.get('from') == qual_id:
                inst_entity = graph.entities_by_id.get(edge.get('to'))
                if inst_entity:
                    inst_name = inst_entity.get('canonical_name', inst_name)
                    
        dates_block = qual.get('dates', {})
        start_val = dates_block.get('start', '')
        end_val = dates_block.get('end', '')
        if isinstance(start_val, dict): start_val = start_val.get('date', '')
        if isinstance(end_val, dict): end_val = end_val.get('date', '')
        # YAML may parse unquoted dates (e.g. 2026-07-09) as datetime.date objects
        start_val = str(start_val) if start_val else ''
        end_val = str(end_val) if end_val else ''
        
        domain["education"].append({
            "id": qual_id,
            "degree_name": degree,
            "institution_name": inst_name,
            "dates": {
                "start_date": start_val,
                "end_date": end_val
            },
            "metadata": {
                "confidence": qual.get('confidence', 'unverified'),
                "evidence_id": None
            },
            "entity_type": qual.get("entity_type", "qualification")
        })
        
    # Map Competencies
    if competencies:
        for comp in competencies:
            domain["competencies"].append({
                "category": comp.get("category"),
                "skills": comp.get("skills", [])
            })
            
    return domain

def build():
    # 1. Clear Artifacts
    if ARTIFACTS_DIR.exists():
        shutil.rmtree(ARTIFACTS_DIR)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 2. Graph Validation (Fails build if corrupt)
    validate_graph()
    
    # 3. Graph Resolution & Profile Domain Model Construction
    graph = load_graph(CAREER_DATA)
    domain_model = build_profile_domain_model(graph)
    
    # Save the intermediate Profile Domain Model (Authoritative Data Path Step 2)
    profile_vm_path = BASE_DIR / "artifacts" / "profile_domain_model.json"
    profile_vm_path.parent.mkdir(exist_ok=True, parents=True)
    with open(profile_vm_path, "w", encoding="utf-8", newline='\n') as f:
        json.dump(domain_model, f, indent=2)
        
    # 4. Verification Resolver
    resolved_states = resolve_verification_state()
    
    # Load claims
    all_claims = {c['id']: c for c in domain_model.get('claims', [])}
    # Also load golden claims directly as fallback, just in case graph doesn't load them correctly
    golden_claims_path = CAREER_DATA / "golden" / "E-001" / "source" / "facts" / "claims.yml"
    if golden_claims_path.exists():
        golden_claims_data = load_yaml(golden_claims_path).get("claims", [])
        for gc in golden_claims_data:
            if gc['id'] not in all_claims:
                all_claims[gc['id']] = gc
    
    policies_doc = load_yaml(POLICIES_PATH)
    policies = policies_doc.get('policies', {})
    verification_rules = policies_doc.get('verification_rules', {})
    
    # 5. Policy Engine & View Model Generation (Authoritative Data Path Step 3)
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
        
        for emp in domain_model.get('employment', []):
            emp_id = emp['id']
            
            # Policy Rule 1: Canonical review_status must be in approved list
            if emp.get('metadata', {}).get('review_status', 'pending') not in approved_emp_statuses:
                continue
                
            start = emp.get('dates', {}).get('start_date', '')
            end = emp.get('dates', {}).get('end_date', 'Present')
            
            exp_entry = {
                "id": emp_id,
                "company": emp.get('employer_name', 'Unknown'),
                "role": emp.get('role_title', 'Unknown'),
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
                        claim_text = highlight.get('text') or all_claims.get(claim_id, {}).get('title', '')
                        if claim_text:
                            exp_entry["bullets"].append(claim_text)
            
            view_model['experience'].append(exp_entry)
            
        # Education / Qualifications
        view_model['qualifications'] = []
        for qual in domain_model.get('education', []):
            qual_id = qual['id']
            if resolved_states.get(qual_id, {}).get('status') == 'VERIFIED':
                start = qual.get("dates", {}).get("start_date", "")
                end = qual.get("dates", {}).get("end_date", "")
                view_model['qualifications'].append({
                    "id": qual_id,
                    "degree": qual.get("degree_name"),
                    "institution": qual.get("institution_name"),
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
