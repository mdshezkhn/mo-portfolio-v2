import re
import yaml
from pathlib import Path

def cross_match():
    root = Path(__file__).resolve().parent.parent
    
    # Load Canonical Facts
    canonical_facts_file = root / "CANONICAL_FACT_TABLE.md"
    
    active_assets = {
        "CV_Master.md": root / "compiled_assets/CV_Master.md",
        "Portfolio_Copy.md": root / "compiled_assets/Portfolio_Copy.md",
        "LinkedIn_Ready_To_Paste.md": root / "compiled_assets/linkedin/LinkedIn_Ready_To_Paste.md",
        "CANONICAL_NARRATIVE.md": root / "career-data/facts/CANONICAL_NARRATIVE.md"
    }
    
    # Load canonical claims allowed_variants map
    claims_dir = root / "career-data/facts/claims"
    allowed_map = {}
    if claims_dir.exists():
        for f in claims_dir.glob("*.yml"):
            cdata = yaml.safe_load(f.read_text(encoding="utf-8"))
            for c in cdata.get("claims", []):
                for v in c.get("allowed_variants", []):
                    norm_v = v.lower().strip()
                    allowed_map[norm_v] = c["id"]
                    
    asset_rows = []
    
    for name, path in active_assets.items():
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        for idx, line in enumerate(lines, 1):
            line_clean = line.strip()
            if not line_clean or line_clean.startswith("#") or line_clean.startswith("---"):
                continue
                
            # Basic assertion extraction heuristic
            norm = line_clean.lower()
            
            status = "UNVERIFIED"
            matched_canonical = "-"
            
            if "11+ years" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-001"
            elif "india and china" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-002"
            elif "cumbria" in norm or "pgce" in norm:
                status = "MATCH"
                matched_canonical = "FACT-QUAL-3002"
            elif "b.ed" in norm or "bachelor of education" in norm:
                status = "MATCH"
                matched_canonical = "FACT-QUAL-3003"
            elif "b.sc" in norm or "physics" in norm:
                status = "MATCH"
                matched_canonical = "FACT-QUAL-3000"
            elif "tesol" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-005"
            elif "tefl" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-006"
            elif "m.a. english" in norm:
                status = "MATCH"
                matched_canonical = "FACT-QUAL-3001"
            elif "moderation" in norm or "grade 5 writing" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-013"
            elif "gedu" in norm or "uk, dubai, and malta" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-017"
            elif "whitehat" in norm or "byju's" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-014"
            elif "eton house" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-019"
            elif "scholars academy" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-024"
            elif "english" in norm and "fluent" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-020"
            elif "hindi" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-021"
            elif "urdu" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-022"
            elif "august 2027" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-023"
            elif "mentor" in norm or "mentoring" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-010"
            elif "curriculum implementation" in norm or "cross-curricular" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-011"
            elif "curriculum development" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-012"
            elif "action research" in norm:
                status = "MATCH"
                matched_canonical = "FACT-C-007"
            elif "rapidly improving" in norm:
                status = "RESTRICTED VIOLATION"
                matched_canonical = "FACT-C-OLD-001"
            elif "curriculum lead" in norm:
                status = "TITLE DRIFT"
                matched_canonical = "FACT-C-OLD-002"
                
            asset_rows.append({
                "asset": name,
                "line": idx,
                "assertion": line_clean,
                "matched_fact": matched_canonical,
                "status": status
            })
            
    # Write ASSET_FACT_TABLE.md
    out_lines = [
        "# ASSET_FACT_TABLE.md",
        "",
        "> **Phase 3 & 4 Audit Deliverable**: Line-by-line factual assertions extracted from active recruiter presentation assets and cross-matched against canonical facts.",
        "",
        "| Asset | Line | Extracted Assertion | Matched Canonical Fact | Classification Status |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for r in asset_rows:
        out_lines.append(f"| `{r['asset']}` | L{r['line']} | {r['assertion']} | `{r['matched_fact']}` | **{r['status']}** |")
        
    Path(root / "ASSET_FACT_TABLE.md").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Parsed {len(asset_rows)} assertions from active assets.")

if __name__ == "__main__":
    cross_match()
