import yaml
from pathlib import Path

def verify_all_dependencies():
    root = Path(__file__).resolve().parent.parent
    
    manifest = yaml.safe_load((root / "evidence/manifest.yml").read_text(encoding="utf-8")).get("entries", {})
    
    claims = []
    claims_dir = root / "career-data/facts/claims"
    if claims_dir.exists():
        for f in claims_dir.glob("*.yml"):
            cdata = yaml.safe_load(f.read_text(encoding="utf-8"))
            claims.extend(cdata.get("claims", []))
            
    emp = yaml.safe_load((root / "career-data/facts/employment.yml").read_text(encoding="utf-8")).get("employment_records", [])
    edu = yaml.safe_load((root / "career-data/facts/education.yml").read_text(encoding="utf-8")).get("education_records", [])
    
    # Collect all evidence IDs referenced
    referenced_ev = set()
    for c in claims:
        for ev in c.get("evidence", []):
            referenced_ev.add(ev)
    for e in emp:
        for ev in e.get("evidence", []):
            referenced_ev.add(ev)
    for q in edu:
        for ev in q.get("evidence", []):
            referenced_ev.add(ev)
            
    manifest_ev = set(manifest.keys())
    
    missing_ev = referenced_ev - manifest_ev
    unused_ev = manifest_ev - referenced_ev
    
    print("=========================================")
    print("        DEPENDENCY VERIFICATION          ")
    print("=========================================")
    print(f"Manifest Evidence IDs:   {len(manifest_ev)}")
    print(f"Referenced Evidence IDs: {len(referenced_ev)}")
    print(f"Missing Evidence IDs:    {len(missing_ev)} -> {list(missing_ev)}")
    print(f"Unused Evidence IDs:     {len(unused_ev)} -> {list(unused_ev)}")
    print("=========================================")
    
    if len(missing_ev) == 0:
        print("Dependency Graph Integrity: PASS")
    else:
        print("Dependency Graph Integrity: FAIL")

if __name__ == "__main__":
    verify_all_dependencies()
