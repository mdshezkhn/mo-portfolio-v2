#!/usr/bin/env python3
"""Impact Analysis Tool for Career OS Evidence Graph.
Answers: 'If evidence ID X changes, what entities, claims, and presentation assets break?'
"""
import yaml
import sys
from pathlib import Path

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_impact_analysis(target_ev_id):
    root = Path(__file__).resolve().parent.parent
    
    manifest_file = root / "evidence" / "manifest.yml"
    claims_dir = root / "career-data" / "facts" / "claims"
    employment_file = root / "career-data" / "facts" / "employment.yml"
    education_file = root / "career-data" / "facts" / "education.yml"
    
    if not manifest_file.exists():
        print("Manifest missing.")
        sys.exit(2)
        
    manifest = load_yaml(manifest_file)
    entries = manifest.get("entries", {})
    
    if target_ev_id not in entries:
        print(f"Evidence ID {target_ev_id} not found in manifest.")
        sys.exit(1)
        
    ev = entries[target_ev_id]
    
    # Trace Claims
    affected_claims = []
    affected_assets = set()
    
    if claims_dir.exists():
        for c_file in claims_dir.glob("*.yml"):
            c_data = load_yaml(c_file)
            for claim in c_data.get("claims", []):
                if target_ev_id in claim.get("evidence", []):
                    affected_claims.append(claim["id"])
                    for asset in claim.get("presentation_assets", []):
                        affected_assets.add(asset)
                        
    # Trace Employment
    affected_employments = []
    if employment_file.exists():
        emp_data = load_yaml(employment_file)
        for emp in emp_data.get("employment_records", []):
            if target_ev_id in emp.get("evidence", []):
                affected_employments.append(emp["id"])
                
    # Trace Education
    affected_qualifications = []
    if education_file.exists():
        edu_data = load_yaml(education_file)
        for qual in edu_data.get("education_records", []):
            if target_ev_id in qual.get("evidence", []):
                affected_qualifications.append(qual["id"])

    print("="*60)
    print(f"       IMPACT ANALYSIS REPORT FOR: {target_ev_id}")
    print("="*60)
    print(f"Description:           {ev.get('description')}")
    print(f"Confidence Level:      {ev.get('confidence')}")
    print(f"File Path:             {ev.get('file')}")
    print("-" * 60)
    print(f"Affected Qualifications: {len(affected_qualifications)} -> {affected_qualifications}")
    print(f"Affected Employment Rec: {len(affected_employments)} -> {affected_employments}")
    print(f"Affected Claims:         {len(affected_claims)} -> {affected_claims}")
    print(f"Affected Assets:         {len(affected_assets)} -> {list(affected_assets)}")
    print("="*60)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "E-3005"
    run_impact_analysis(target)
