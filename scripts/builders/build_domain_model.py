import json
import argparse
from pathlib import Path

def build_domain_model(graph):
    # Retrieve base identities
    identity = list(graph.all().by_type('identity'))
    identity = identity[0] if identity else graph.entities_by_id.get('PERSON-1000', {})
    
    # Core domain entities
    employments = list(graph.employments())
    # Sort employments by start date newest first as a semantic invariant
    employments = sorted(employments, key=lambda e: e.get('dates', {}).get('start', ''), reverse=True)
    
    qualifications = list(graph.qualifications())
    
    claims = list(graph.claims())
    competencies = list(graph.all().by_type('competencie'))  # entity_type = 'competencie' (due to rstrip('s') in resolve_graph.py)
    
    master_path = Path(__file__).parent.parent.parent / "templates" / "cv" / "profiles" / "master.json"
    master_data = {}
    if master_path.exists():
        import json
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
                "evidence_id": evidence_id
            }
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
            }
        })
        
    # Map Competencies
    if not competencies:
        pass
    else:
        for comp in competencies:
            domain["competencies"].append({
                "category": comp.get("category"),
                "skills": comp.get("skills", [])
            })
            
    return domain

if __name__ == "__main__":
    import sys
    # Add parent dir to path for imports
    sys.path.append(str(Path(__file__).parent.parent))
    from query_engine import load_graph
    
    parser = argparse.ArgumentParser(description="Build Domain Model")
    parser.add_argument("--data-dir", default="career-data")
    args = parser.parse_args()
    
    graph = load_graph(args.data_dir)
    domain_model = build_domain_model(graph)
    
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    
    output_path = artifacts_dir / "profile_domain_model.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(domain_model, f, indent=2)
        
    print(f"Generated Domain Model at {output_path}")
