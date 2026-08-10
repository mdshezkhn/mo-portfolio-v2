import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(BASE_DIR, "artifacts", "cv_view_models")
PARTIALS_DIR = os.path.join(BASE_DIR, "templates", "cv", "partials")
BASE_TEMPLATE = os.path.join(BASE_DIR, "templates", "cv", "base.html")
OUTPUT_DIR = os.path.join(BASE_DIR, "compiled_assets")

def load_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def build_experience_html(experience_data):
    html = ""
    for entry in experience_data:
        html += f"""        <div class="entry">
            <div class="entry-header">
                <span class="entry-title">{entry['company']}</span>
                <span class="entry-date">{entry['date']}</span>
            </div>
            <ul>\n"""
        for bullet in entry['bullets']:
            html += f"                <li>{bullet}</li>\n"
        html += "            </ul>\n        </div>\n"
    return html

def build_list_html(items):
    return "\n".join([f"            <li>{item}</li>" for item in items])

def main():
    if os.path.exists(OUTPUT_DIR):
        import shutil
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
        
    base_html = load_file(BASE_TEMPLATE)
    summary_partial = load_file(os.path.join(PARTIALS_DIR, "summary.html"))
    competencies_partial = load_file(os.path.join(PARTIALS_DIR, "competencies.html"))
    experience_partial = load_file(os.path.join(PARTIALS_DIR, "experience.html"))
    education_partial = load_file(os.path.join(PARTIALS_DIR, "education.html"))
    languages_partial = load_file(os.path.join(PARTIALS_DIR, "languages.html"))
    contact_partial = load_file(os.path.join(PARTIALS_DIR, "contact.html"))
    
    current_date = datetime.now().strftime("%Y-%m-%d")

    for filename in os.listdir(PROFILES_DIR):
        if not filename.endswith(".json"):
            continue
            
        with open(os.path.join(PROFILES_DIR, filename), "r", encoding="utf-8") as f:
            profile = json.load(f)
            
        print(f"Building {filename}...")
        
        # Build sections
        summary_html = summary_partial.replace("{SUMMARY_TEXT}", profile.get("summary", ""))
        
        comp_list = build_list_html(profile.get("competencies", []))
        comp_html = competencies_partial.replace("{COMPETENCIES_LIST}", comp_list)
        
        exp_entries = build_experience_html(profile.get("experience", []))
        exp_html = experience_partial.replace("{EXPERIENCE_ENTRIES}", exp_entries)
        
        edu_list = build_list_html(profile.get("education", []))
        edu_html = education_partial.replace("{EDUCATION_LIST}", edu_list)
        
        lang_list = build_list_html(profile.get("languages", []))
        lang_html = languages_partial.replace("{LANGUAGES_LIST}", lang_list) if profile.get("languages") else ""
        
        # Build contact
        contact = profile.get("contact", {})
        phone_pres = "Phone provided on PDF download" if contact.get("phone_status") == "download_only" else contact.get("phone", "")
        contact_html = contact_partial.replace("{AVAILABILITY}", contact.get("availability", "")).replace("{PHONE_PRESENTATION}", phone_pres)
        
        # Inject into base
        final_html = base_html
        final_html = final_html.replace("{TITLE}", profile.get("title", ""))
        final_html = final_html.replace("{ASSET_NAME}", profile.get("asset_name", ""))
        final_html = final_html.replace("{CLAIMS}", ", ".join(profile.get("claims", [])))
        final_html = final_html.replace("{DATE}", current_date)
        final_html = final_html.replace("{SUBTITLE}", profile.get("subtitle", ""))
        final_html = final_html.replace("{CONTACT_PRESENTATION}", contact_html)
        
        final_html = final_html.replace("{SUMMARY}", summary_html)
        final_html = final_html.replace("{COMPETENCIES}", comp_html)
        final_html = final_html.replace("{EXPERIENCE}", exp_html)
        final_html = final_html.replace("{EDUCATION}", edu_html)
        final_html = final_html.replace("{LANGUAGES}", lang_html)
        
        out_filename = f"CV_{profile.get('title', 'Doc').replace(' ', '_').replace('/', '_')}.html"
        out_filepath = os.path.join(OUTPUT_DIR, out_filename)
        
        with open(out_filepath, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print(f"-> Generated {out_filename}")

if __name__ == "__main__":
    main()
