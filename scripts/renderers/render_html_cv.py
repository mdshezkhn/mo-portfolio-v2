import json
import os
from datetime import datetime
from pathlib import Path

def load_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def build_experience_html(experience_data):
    html = ""
    for entry in experience_data:
        html += f"""        <div class="entry">
            <div class="entry-header">
                <span class="entry-title">{entry['employer_name']}</span>
                <span class="entry-date">{entry['date_range']}</span>
            </div>
            <div class="entry-role"><strong>{entry.get('role_title', '')}</strong></div>
            <ul>\n"""
        for bullet in entry['highlights']:
            html += f"                <li>{bullet}</li>\n"
        html += "            </ul>\n        </div>\n"
    return html

def build_list_html(items):
    return "\n".join([f"            <li>{item}</li>" for item in items])

def render_html(cv_vm):
    root = Path(__file__).parent.parent.parent
    partials_dir = root / "templates" / "cv" / "partials"
    base_template = root / "templates" / "cv" / "base.html"
    
    base_html = load_file(base_template)
    summary_partial = load_file(partials_dir / "summary.html")
    competencies_partial = load_file(partials_dir / "competencies.html")
    experience_partial = load_file(partials_dir / "experience.html")
    education_partial = load_file(partials_dir / "education.html")
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Render sections
    summary_text = "\n".join(cv_vm.get("summary", []))
    summary_html = summary_partial.replace("{SUMMARY_TEXT}", summary_text)
    
    comp_list = build_list_html(cv_vm.get("competencies", []))
    comp_html = competencies_partial.replace("{COMPETENCIES_LIST}", comp_list)
    
    exp_entries = build_experience_html(cv_vm.get("experience", []))
    exp_html = experience_partial.replace("{EXPERIENCE_ENTRIES}", exp_entries)
    
    # The legacy renderer didn't actually pull "details" or use object formatting for education, 
    # it just used strings. Wait, in cv_vm, education is an array of objects. 
    # But legacy education was just an array of strings. Let's adapt it:
    edu_strings = []
    for ed in cv_vm.get("education", []):
        if not ed.get('institution_name'):
            # Fallback exact string
            edu_strings.append(ed['degree_name'])
        else:
            s = f"{ed['degree_name']}, {ed['institution_name']}"
            if ed.get('date_range') and ed['date_range'] != 'Present':
                s += f" ({ed['date_range']})"
            edu_strings.append(s)
        
    edu_list = build_list_html(edu_strings)
    edu_html = education_partial.replace("{EDUCATION_LIST}", edu_list)
    
    final_html = base_html
    header = cv_vm.get("header", {})
    final_html = final_html.replace("{TITLE}", header.get("title", ""))
    final_html = final_html.replace("{SUBTITLE}", header.get("subtitle", "") or header.get("title", ""))
    
    # Dummy manifest values for now, as cv_vm is decoupled from builder specifics
    final_html = final_html.replace("{ASSET_NAME}", "CV_Master_v2")
    final_html = final_html.replace("{CLAIMS}", "Migrated to V2")
    final_html = final_html.replace("{DATE}", current_date)
    
    final_html = final_html.replace("{SUMMARY}", summary_html)
    final_html = final_html.replace("{COMPETENCIES}", comp_html)
    final_html = final_html.replace("{EXPERIENCE}", exp_html)
    final_html = final_html.replace("{EDUCATION}", edu_html)
    
    # Resolve remaining placeholders that don't have dynamic content yet
    final_html = final_html.replace("{CONTACT_PRESENTATION}", "")
    final_html = final_html.replace("{LANGUAGES}", "")
    
    return final_html

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--vm-file", default="artifacts/cv_vm.json")
    parser.add_argument("--out", default="artifacts/generated/cv_v2.html")
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent.parent
    vm_path = root / args.vm_file
    
    with open(vm_path, "r", encoding="utf-8") as f:
        cv_vm = json.load(f)
        
    html_out = render_html(cv_vm)
    
    out_path = root / args.out
    out_path.parent.mkdir(exist_ok=True, parents=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
        
    print(f"Rendered HTML CV to {args.out}")
