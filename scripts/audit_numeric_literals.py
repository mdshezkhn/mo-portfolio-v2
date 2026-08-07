import re
import yaml
from pathlib import Path

def audit_numeric_literals():
    root = Path(__file__).resolve().parent.parent
    
    # Patterns to match recruiter-facing numeric literals
    patterns = [
        r'\b\d+\+\s*years\b',
        r'\b\d+\+\s*educators\b',
        r'\b\d+\+\s*trainers\b',
        r'\b\d+\s*schools\b',
        r'\b\d+\s*employers\b',
        r'\b\d+\s*countries\b',
        r'\b\d+\s*degrees\b',
        r'\baugust\s*202\d\b',
        r'\b\d{4}\s*–\s*\d{4}\b',
        r'\b\d{4}\s*-\s*\d{4}\b',
        r'class="stat-number">\s*\d+\+?\s*<',
        r'class="stat-num">\s*\d+\+?\s*<'
    ]
    
    findings = []
    
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        if any(part in rel for part in ['.git', '.playwright-mcp', '.pytest_cache', 'brain', '.claude', 'node_modules']):
            continue
            
        ext = path.suffix.lower()
        if ext not in ['.md', '.html', '.json', '.js', '.css', '.yml', '.yaml']:
            continue
            
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue
            
        lines = content.split("\n")
        for idx, line in enumerate(lines, 1):
            line_str = line.strip()
            for p in patterns:
                matches = re.findall(p, line_str, flags=re.IGNORECASE)
                for m in matches:
                    # Determine classification
                    if "career-data/facts" in rel or "evidence/" in rel or "governance/" in rel:
                        ctype = "CANONICAL (Source YAML)"
                        action = "Preserve as Ground Truth"
                    elif "compiled_assets/" in rel or "RELEASE_2027" in rel:
                        ctype = "COMPUTED (Generated)"
                        action = "Preserve as Generated Output"
                    elif "mo-portfolio-v2/index.html" in rel:
                        ctype = "SYNCHRONIZED HTML"
                        action = "Synchronized to C-001 / Canonical"
                    elif "archive/" in rel or "cv.md" in rel or "linkedin.md" in rel:
                        ctype = "DEPRECATED LEGACY"
                        action = "Flagged in LEGACY_CONTENT_REPORT.md"
                    else:
                        ctype = "HARD-CODED ASSET"
                        action = "Review for Build Template Generator"
                        
                    findings.append({
                        "file": rel,
                        "line": idx,
                        "literal": m,
                        "snippet": line_str[:120],
                        "classification": ctype,
                        "action": action
                    })
                    
    # Generate HARDCODED_NUMERIC_FACT_AUDIT.md
    out_lines = [
        "# HARDCODED_NUMERIC_FACT_AUDIT.md",
        "",
        "> **Repository-Wide Forensic Audit**: Inventory of every recruiter-facing numeric literal across HTML, Markdown, JSON, JS, CSS, and YAML assets.",
        "",
        "| File Path | Line | Numeric Literal Extracted | Context Snippet | Classification | Governance Action |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for f in findings:
        out_lines.append(f"| `{f['file']}` | L{f['line']} | `{f['literal']}` | {f['snippet']} | **{f['classification']}** | {f['action']} |")
        
    Path(root / "HARDCODED_NUMERIC_FACT_AUDIT.md").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Scanned repository for numeric literals. Found {len(findings)} matches.")

if __name__ == "__main__":
    audit_numeric_literals()
