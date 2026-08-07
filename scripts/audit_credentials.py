from pathlib import Path
import yaml

def audit_credentials():
    root = Path(__file__).resolve().parent.parent
    
    edu_file = root / "career-data" / "facts" / "education.yml"
    manifest_file = root / "evidence" / "manifest.yml"
    
    edu = yaml.safe_load(edu_file.read_text(encoding="utf-8")).get("education_records", [])
    manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8")).get("entries", {})
    
    print("=== CANONICAL EDUCATION & CERTIFICATE RECORDS ===")
    for q in edu:
        print(f"ID: {q['id']} | Degree: {q['degree']} | Inst: {q['institution_id']} | Conf: {q.get('confidence')} | Ev: {q.get('evidence', [])}")
        
    print("\n=== EVIDENCE MANIFEST ENTRIES ===")
    for eid, edata in manifest.items():
        if "cert" in edata.get("description", "").lower() or "pgce" in edata.get("description", "").lower() or "degree" in edata.get("description", "").lower() or "tesol" in edata.get("description", "").lower() or "tefl" in edata.get("description", "").lower():
            print(f"ID: {eid} | File: {edata.get('file')} | Desc: {edata.get('description')} | Conf: {edata.get('confidence')} | Verified: {edata.get('verified')}")

if __name__ == "__main__":
    audit_credentials()
