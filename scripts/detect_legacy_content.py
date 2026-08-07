from pathlib import Path
import re

def detect_legacy_content():
    root = Path(__file__).resolve().parent.parent
    
    active_assets = [
        "compiled_assets/CV_Master.md",
        "compiled_assets/CV_Teacher_Development.md",
        "compiled_assets/Portfolio_Copy.md",
        "compiled_assets/linkedin/LinkedIn_Ready_To_Paste.md",
        "career-data/facts/CANONICAL_NARRATIVE.md"
    ]
    
    triggers = ["rapidly improving", "curriculum lead", "proven track record", "specialist in", "15+ years", "led a nationwide"]
    
    findings = []
    
    for path in root.rglob("*.md"):
        rel = str(path.relative_to(root)).replace("\\", "/")
        if any(part in rel for part in ['.git', '.playwright-mcp', 'brain', '.claude']):
            continue
            
        if rel in active_assets:
            continue # Skip active assets
            
        content = path.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        for idx, line in enumerate(lines, 1):
            line_low = line.lower()
            for t in triggers:
                if t in line_low:
                    findings.append({
                        "file": rel,
                        "line": idx,
                        "trigger": t,
                        "sentence": line.strip()
                    })
                    
    lines = [
        "# LEGACY_CONTENT_REPORT.md",
        "",
        "> **Phase 11 Audit Deliverable**: Forensic inventory of legacy marketing language, title inflation, and unverified outcome claims in non-active repository files.",
        "",
        "| File Path | Line | Risk Trigger | Sentence Snippet | Status |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for f in findings:
        lines.append(f"| `{f['file']}` | L{f['line']} | `{f['trigger']}` | {f['sentence']} | **DEPRECATED / DO NOT PUBLISH** |")
        
    Path(root / "LEGACY_CONTENT_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Detected {len(findings)} legacy content risks across non-active files.")

if __name__ == "__main__":
    detect_legacy_content()
