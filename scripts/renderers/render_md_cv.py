import json
import os
from pathlib import Path

def render_md(cv_vm):
    md = []
    
    header = cv_vm.get("header", {})
    name = header.get("name", "")
    title = header.get("title", "")
    md.append(f"# {name}")
    if title:
        md.append(f"**{title}**")
    
    # To match base.html which hardcodes this
    md.append("Available from August 2027")
    
    md.append("")
    md.append("## Professional Summary")
    summary = "\n\n".join(cv_vm.get("summary", []))
    md.append(summary)
    md.append("")
    
    md.append("## Core Expertise")
    for comp in cv_vm.get("competencies", []):
        md.append(f"* {comp}")
    md.append("")
    
    md.append("## Professional Experience")
    for exp in cv_vm.get("experience", []):
        md.append("")
        title = exp.get("employer_name", "")
        dates = exp.get("date_range", "")
        role = exp.get("role_title", "")
        
        # Legacy formatting: "### Company (Dates)"
        header_str = f"### {title}"
        if dates:
            header_str += f" ({dates})"
        md.append(header_str)
        
        if role:
            md.append(f"**{role}**")
            
        for bullet in exp.get("highlights", []):
            md.append(f"* {bullet}")
    md.append("")
    
    md.append("## Education & Qualifications")
    for ed in cv_vm.get("education", []):
        if not ed.get('institution_name'):
            # Fallback exact string
            md.append(f"* {ed['degree_name']}")
        else:
            s = f"{ed['degree_name']}, {ed['institution_name']}"
            if ed.get('date_range') and ed['date_range'] != 'Present':
                s += f" ({ed['date_range']})"
            md.append(f"* {s}")
            
    return "\n".join(md) + "\n"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--vm-file", default="artifacts/cv_vm.json")
    parser.add_argument("--out", default="artifacts/generated/cv_v2.md")
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent.parent
    vm_path = root / args.vm_file
    
    with open(vm_path, "r", encoding="utf-8") as f:
        cv_vm = json.load(f)
        
    md_out = render_md(cv_vm)
    
    out_path = root / args.out
    out_path.parent.mkdir(exist_ok=True, parents=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_out)
        
    print(f"Rendered MD CV to {args.out}")
