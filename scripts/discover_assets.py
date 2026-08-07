import os
import yaml
from pathlib import Path
from datetime import datetime

def discover_assets():
    root = Path(__file__).resolve().parent.parent
    
    active_assets = [
        "compiled_assets/CV_Master.md",
        "compiled_assets/CV_Teacher_Development.md",
        "compiled_assets/Portfolio_Copy.md",
        "compiled_assets/linkedin/LinkedIn_Ready_To_Paste.md",
        "career-data/facts/CANONICAL_NARRATIVE.md"
    ]
    
    rows = []
    
    for path in root.rglob("*"):
        if path.is_file():
            rel_path = str(path.relative_to(root)).replace("\\", "/")
            if any(part in rel_path for part in ['.git', '.playwright-mcp', '.pytest_cache', 'brain', '.claude']):
                continue
                
            ext = path.suffix.lower()
            if ext in ['.md', '.yml', '.yaml', '.json', '.html']:
                # Determine purpose & status
                status = "Active" if rel_path in active_assets else "Governance / Support"
                if "archive" in rel_path or "backup" in rel_path or rel_path.startswith("cv") or rel_path.startswith("linkedin"):
                    if rel_path not in active_assets and ext == '.md':
                        status = "Deprecated / Legacy"
                        
                gen = "Generated" if rel_path.startswith("compiled_assets") or rel_path == "CLAIM_REGISTER.md" else "Manual / Canonical"
                
                mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d')
                
                rows.append({
                    "asset": rel_path,
                    "purpose": get_purpose(rel_path),
                    "status": status,
                    "generated": gen,
                    "modified": mtime
                })
                
    # Write REPOSITORY_ASSET_INDEX.md
    out_lines = [
        "# REPOSITORY_ASSET_INDEX.md",
        "",
        "> **Phase 1 Audit Deliverable**: Comprehensive inventory of all Markdown, YAML, JSON, and HTML assets across the Career OS repository.",
        "",
        "| Asset Path | Purpose | Status | Generation Type | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for r in sorted(rows, key=lambda x: x["asset"]):
        out_lines.append(f"| `{r['asset']}` | {r['purpose']} | **{r['status']}** | {r['generated']} | {r['modified']} |")
        
    Path(root / "REPOSITORY_ASSET_INDEX.md").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Discovered {len(rows)} assets.")

def get_purpose(path):
    if "compiled_assets/CV_Master.md" in path: return "Primary Recruiter Master CV"
    if "compiled_assets/Portfolio_Copy.md" in path: return "Public Portfolio Copy"
    if "LinkedIn_Ready_To_Paste" in path: return "LinkedIn Profile Copy"
    if "CANONICAL_NARRATIVE" in path: return "Canonical Positioning & Narrative Authority"
    if "claims" in path: return "Canonical Claim Registry"
    if "employment.yml" in path: return "Governed Employment Facts"
    if "education.yml" in path: return "Governed Education Facts"
    if "organisations.yml" in path: return "Governed Organisation Facts"
    if "institutions.yml" in path: return "Governed Institution Facts"
    if "manifest.yml" in path: return "Governed Evidence Manifest"
    if "archive" in path: return "Archived Historical Asset"
    if "scripts" in path: return "Governance / Automation Engine"
    return "Repository Documentation / Data"

if __name__ == "__main__":
    discover_assets()
