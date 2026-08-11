import json
import yaml
import sys
from datetime import datetime
from pathlib import Path

def get_in(data, path_str):
    parts = path_str.split('.')
    current = data
    for p in parts:
        if isinstance(current, dict) and p in current:
            current = current[p]
        else:
            return None
    return current

def format_date_range(start_date, end_date):
    def fmt(d):
        if not d or d == 'UNKNOWN': return 'Present'
        try:
            return datetime.strptime(d, '%Y-%m-%d').strftime('%b %Y')
        except ValueError:
            try:
                return datetime.strptime(d, '%Y-%m').strftime('%b %Y')
            except ValueError:
                return d
    start = fmt(start_date)
    end = fmt(end_date)
    if start == end:
        return start
    return f"{start} - {end}"

def apply_mapping(domain_model, mapping):
    vm = {
        "header": {},
        "summary": [],
        "competencies": [],
        "experience": [],
        "education": []
    }
    
    # Simple explicit traversal according to mapping 
    # to maintain functional purity and declarative logic
    
    # Header
    vm["header"]["name"] = get_in(domain_model, mapping["header.name"]["source"])
    vm["header"]["title"] = get_in(domain_model, mapping["header.title"]["source"])
    vm["header"]["subtitle"] = get_in(domain_model, mapping["header.subtitle"]["source"])
    
    # Summary
    sum_map = mapping["summary"]
    if sum_map.get("operation") == "copy":
        val = get_in(domain_model, sum_map["source"])
        # ensure it's a list if it's a string since schema expects an array?
        # Wait, cv_vm.schema.json expects an array of strings for summary? Let me check that.
        vm["summary"] = [val] if isinstance(val, str) else val
    elif sum_map.get("operation") == "extract":
        priorities = sum_map["filter"]["priority"]
        for claim in domain_model.get("claims", []):
            if claim.get("priority") in priorities:
                vm["summary"].append(claim.get(sum_map["field"]))
            
    # Competencies
    comp_map = mapping["competencies"]
    for comp in domain_model.get("competencies", []):
        vm["competencies"].extend(comp.get(comp_map["field"], []))
        
    # Experience
    claims_by_id = {c["id"]: c for c in domain_model.get("claims", [])}
    for emp in domain_model.get("employment", []):
        exp = {
            "id": emp["id"],
            "role_title": emp["role_title"],
            "employer_name": emp["employer_name"],
            "date_range": emp.get("master_date") or format_date_range(
                emp.get("dates", {}).get("start_date"), 
                emp.get("dates", {}).get("end_date")
            ),
            "highlights": []
        }
        for cid in emp.get("supported_claims", []):
            if cid in claims_by_id:
                stmt = claims_by_id[cid].get("title")
                if stmt: exp["highlights"].append(stmt)
            else:
                exp["highlights"].append(cid)
        vm["experience"].append(exp)
        
    # Education
    for edu in domain_model.get("education", []):
        ed = {
            "id": edu["id"],
            "degree_name": edu["degree_name"],
            "institution_name": edu["institution_name"],
            "date_range": format_date_range(
                edu.get("dates", {}).get("start_date"), 
                edu.get("dates", {}).get("end_date")
            ),
            "details": ""
        }
        vm["education"].append(ed)
        
    vm["_meta"] = {
        "schema_version": "1.0",
        "producer_version": "1.0",
        "generator": "project_cv_vm.py"
    }
    
    return vm

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default="artifacts/profile_domain_model.json")
    parser.add_argument("--mapping", default="contracts/cv_field_map.yaml")
    parser.add_argument("--out", default="artifacts/cv_vm.json")
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent.parent
    
    with open(root / args.domain, "r", encoding="utf-8") as f:
        domain = json.load(f)
        
    with open(root / args.mapping, "r", encoding="utf-8") as f:
        mapping = yaml.safe_load(f)
        
    cv_vm = apply_mapping(domain, mapping)
    
    out_path = root / args.out
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cv_vm, f, indent=2)
        
    print(f"Projected CV VM to {args.out}")
