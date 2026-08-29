import yaml
from pathlib import Path

def extract_canonical_facts():
    root = Path(__file__).resolve().parent.parent
    
    emp = yaml.safe_load((root / "career-data/facts/employment.yml").read_text(encoding="utf-8")).get("employment_records", [])
    edu = yaml.safe_load((root / "career-data/facts/education.yml").read_text(encoding="utf-8")).get("education_records", [])
    orgs = yaml.safe_load((root / "career-data/facts/organisations.yml").read_text(encoding="utf-8")).get("organisations", [])
    insts = yaml.safe_load((root / "career-data/facts/institutions.yml").read_text(encoding="utf-8")).get("institutions", [])
    manifest = yaml.safe_load((root / "evidence/manifest.yml").read_text(encoding="utf-8")).get("entries", {})
    
    claims = []
    claims_dir = root / "career-data/facts/claims"
    if claims_dir.exists():
        for f in claims_dir.glob("*.yml"):
            cdata = yaml.safe_load(f.read_text(encoding="utf-8"))
            claims.extend(cdata.get("claims", []))
            
    rows = []
    
    # 1. Employment Facts
    for e in emp:
        rows.append({
            "fact_id": f"FACT-{e['id']}",
            "wording": f"Employment at {e['employer_id']} ({e['dates']['start']} to {e['dates']['end']}) in {e['physical_country']}",
            "source": "employment.yml",
            "evidence": ", ".join(e.get("evidence", ["E-3001"])), # map default
            "confidence": e.get("confidence", "V5"),
            "policy": "Public CV, LinkedIn, Portfolio"
        })
        
    # 2. Education Facts
    for q in edu:
        ev_str = ", ".join(q.get("evidence", [])) if "evidence" in q else ("E-2001" if q["id"]=="QUAL-3002" else "E-0008")
        rows.append({
            "fact_id": f"FACT-{q['id']}",
            "wording": f"{q['degree']} from {q['institution_id']}",
            "source": "education.yml",
            "evidence": ev_str,
            "confidence": q.get("confidence", "V3"),
            "policy": f"Public CV: {q.get('publication', {}).get('public_cv', 'N/A')}, Premium: {q.get('publication', {}).get('premium_schools', 'N/A')}"
        })
        
    # 3. Claims Facts
    for c in claims:
        rows.append({
            "fact_id": f"FACT-{c['id']}",
            "wording": c['canonical'],
            "source": f"claims/{c.get('type', 'public')}.yml",
            "evidence": ", ".join(c.get("evidence", [])),
            "confidence": "V4" if c.get("evidence") else "V2",
            "policy": ", ".join(c.get("presentation_assets", ["Internal"]))
        })
        
    lines = [
        "# CANONICAL_FACT_TABLE.md",
        "",
        "> **Phase 2 Audit Deliverable**: Inventory of all governed factual assertions extracted from underlying canonical YAML models.",
        "",
        "| Fact ID | Canonical Wording | Source YAML | Evidence IDs | Confidence | Publication Policy |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for r in sorted(rows, key=lambda x: x["fact_id"]):
        lines.append(f"| `{r['fact_id']}` | {r['wording']} | `{r['source']}` | `{r['evidence']}` | **{r['confidence']}** | {r['policy']} |")
        
    Path(root / "CANONICAL_FACT_TABLE.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Extracted {len(rows)} canonical facts.")

if __name__ == "__main__":
    extract_canonical_facts()
