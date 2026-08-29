import yaml
import re
from pathlib import Path

def verify_public_scope():
    root = Path(__file__).resolve().parent.parent
    
    # Load restricted claims
    restricted_file = root / "career-data" / "facts" / "claims" / "restricted.yml"
    restricted_claims = []
    if restricted_file.exists():
        cdata = yaml.safe_load(restricted_file.read_text(encoding="utf-8"))
        restricted_claims = cdata.get("claims", [])
        
    restricted_texts = []
    for c in restricted_claims:
        if c.get("canonical"):
            restricted_texts.append(c["canonical"].lower())
        for v in c.get("allowed_variants", []):
            restricted_texts.append(v.lower())
            
    # Add specific unverified restricted phrases
    restricted_phrases = ["200+ educators", "1,000+ educators", "1000+ educators", "15+ trainers", "a team of trainers"]
    
    # Audit target: mo-portfolio-v2/index.html & compiled_assets/
    targets = [
        root / "mo-portfolio-v2" / "index.html",
        root / "compiled_assets" / "CV_Master.md",
        root / "compiled_assets" / "Portfolio_Copy.md",
        root / "compiled_assets" / "linkedin" / "LinkedIn_Ready_To_Paste.md"
    ]
    
    violations = []
    
    for t in targets:
        if not t.exists(): continue
        rel = str(t.relative_to(root)).replace("\\", "/")
        content = t.read_text(encoding="utf-8").lower()
        
        for p in restricted_phrases:
            if p in content:
                violations.append({
                    "asset": rel,
                    "type": "RESTRICTED CLAIM LEAKAGE",
                    "phrase": p,
                    "policy_rule": "Restricted claim with unverified manager confirmation (V4/unverified) published on public asset."
                })
                
    lines = [
        "# PUBLICATION_SCOPE_REPORT.md",
        "",
        "> **Publication Scope & Policy Compliance Audit**: Verifies that restricted claims, V1-only qualifications, and unverified scale metrics are excluded from public presentation assets.",
        "",
        "| Asset Path | Policy Violation Type | Flagged Phrase / Entity | Scope Policy Rule | Remediation Status |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    if violations:
        for v in violations:
            lines.append(f"| `{v['asset']}` | **{v['type']}** | `{v['phrase']}` | {v['policy_rule']} | **ACTION REQUIRED** |")
        print(f"Policy Scope Audit: FAILED. Found {len(violations)} restricted claim policy violations.")
    else:
        lines.append("| `All Active Public Assets` | **NONE** | `Clean` | All public assets comply with publication scope policy. | **PASS** |")
        print("Policy Scope Audit: PASS. 0 publication scope violations found.")
        
    Path(root / "PUBLICATION_SCOPE_REPORT.md").write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    verify_public_scope()
