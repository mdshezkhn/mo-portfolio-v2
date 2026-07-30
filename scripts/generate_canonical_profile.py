import yaml
from pathlib import Path

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_markdown(data_dir, out_path):
    # Load identity
    identity = load_yaml(data_dir / 'facts' / 'identity.yml')
    name = identity.get('name', 'Unknown')
    title = identity.get('title', 'Unknown')
    
    # Load metadata
    metadata = load_yaml(data_dir / 'metadata.yml')
    last_reviewed = metadata.get('last_reviewed', 'Unknown')
    
    # Load roles
    roles = {}
    roles_path = data_dir / 'facts' / 'roles.yml'
    if roles_path.exists():
        roles_data = load_yaml(roles_path)
        for r in roles_data.get('roles', []):
            roles[r['id']] = r['title']

    md_content = f"""# Canonical Career Profile

> **AUTO-GENERATED FILE**: Do not edit manually.
> Generated from `career-data/` YAML files.
> Last Reviewed: {last_reviewed}

## 1. Identity
**Name:** {name}  
**Title:** {title}  

---

## 2. Immutable Employment Records

"""

    emp_path = data_dir / 'facts' / 'employment.yml'
    if emp_path.exists():
        emp_data = load_yaml(emp_path)
        for idx, emp in enumerate(emp_data.get('employment_records', [])):
            role_title = roles.get(emp.get('role_id'), emp.get('role_id'))
            
            # Format dates
            dates = emp.get('dates', {})
            start_date = dates.get('start', {}).get('date', 'Unknown')
            end_date = 'Present' if dates.get('end', {}).get('present') else dates.get('end', {}).get('date', 'Unknown')
            
            md_content += f"### Employment #{idx + 1}\n"
            md_content += f"**Employer:** {emp.get('employer')} ({emp.get('employer_id')})\n"
            md_content += f"- **Role:** {role_title}\n"
            md_content += f"- **Date:** {start_date} – {end_date}\n"
            md_content += f"**Location:** {emp.get('location')}\n"
            md_content += f"**Confidence:** {emp.get('confidence')} | **Review Status:** {emp.get('review_status')}\n\n"
            
    md_content += "---\n\n## 3. Education Records\n\n"
    
    edu_path = data_dir / 'facts' / 'education.yml'
    if edu_path.exists():
        edu_data = load_yaml(edu_path)
        for idx, edu in enumerate(edu_data.get('education_records', [])):
            dates = edu.get('dates', {})
            start_date = dates.get('start', {}).get('date', 'Unknown')
            end_date = 'Present' if dates.get('end', {}).get('present') else dates.get('end', {}).get('date', 'Unknown')
            
            md_content += f"### {edu.get('degree')}\n"
            md_content += f"**Institution:** {edu.get('institution')} ({edu.get('institution_id')})\n"
            md_content += f"**Date:** {start_date} – {end_date}\n"
            md_content += f"**Confidence:** {edu.get('confidence')} | **Review Status:** {edu.get('review_status')}\n\n"

    tp_path = data_dir / 'narratives' / 'teaching_philosophy.yml'
    if tp_path.exists():
        tp_data = load_yaml(tp_path).get('teaching_philosophy', {})
        md_content += "---\n\n## 4. Teaching Philosophy\n\n"
        md_content += f"_{tp_data.get('content', '').strip()}_\n\n"

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

if __name__ == "__main__":
    root = Path(__file__).parent.parent
    data_dir = root / 'career-data'
    out_path = root / 'CANONICAL_PROFILE.md'
    generate_markdown(data_dir, out_path)
    print(f"Generated {out_path} from YAML source of truth.")
