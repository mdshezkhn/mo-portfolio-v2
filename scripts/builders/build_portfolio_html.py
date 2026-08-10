import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
PORTFOLIO_VM_PATH = BASE_DIR / "artifacts" / "cv_view_models" / "portfolio.json"
INDEX_HTML_PATH = BASE_DIR / "mo-portfolio-v2" / "index.html"

def render_experience(exp):
    year = exp.get("date", "").split(" - ")[0].split("-")[0] if exp.get("date") else "Unknown"
    
    html = f"""
                    <div class="tl-item" data-id="{exp['id']}">
                        <time class="tl-year" datetime="{year}">{year}</time>
                        <div class="tl-dot"></div>
                        <div class="tl-card">
                            <div class="tl-card-layout">
                                <div class="tl-main">
                                    <div class="tl-top">
                                        <h3 class="tl-title">{exp['role']}</h3>
                                        <time class="tl-date" datetime="{exp['date']}">{exp['date']}</time>
                                    </div>
                                    <p class="tl-org">{exp['company']}</p>
"""
    if exp.get("bullets"):
        html += f"""
                                    <ul style="padding-left: 20px; font-size: 0.95rem; color: var(--text-secondary); margin-top: 1rem;">
"""
        for b in exp["bullets"]:
            html += f"                                        <li>{b}</li>\n"
        html += """                                    </ul>
"""
    
    html += """                                </div>
                            </div>
                        </div>
                    </div>"""
    return html

def render_qualification(qual):
    cert_id = qual['id'].lower()
    html = f"""
                    <div class="edu-card" data-cert-id="{cert_id}" data-title="{qual['degree']}" data-issuer="{qual['institution']}" data-status="Verified Qualification">
                        <div class="cert-thumb">
                            <span class="cert-thumb-overlay">🔍 View document</span>
                        </div>
                        <h4 class="edu-title">{qual['degree']}</h4>
                        <p class="edu-sch">{qual['institution']}</p>
                        <time class="edu-yr">{qual['date']}</time>
                        <div class="verification-panel">
                            <span class="v-badge">✓ Verified Qualification</span>
                            <div class="v-details">Officially verified by provenance engine.</div>
                        </div>
                    </div>"""
    return html

def build_portfolio_html():
    if not PORTFOLIO_VM_PATH.exists():
        print("Portfolio View Model not found. Did the build_domain_model.py run?")
        return
        
    with open(PORTFOLIO_VM_PATH, "r", encoding="utf-8") as f:
        vm = json.load(f)
        
    exp_html = "\n".join([render_experience(e) for e in vm.get("experience", [])])
    edu_html = "\n".join([render_qualification(q) for q in vm.get("qualifications", [])])
    
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace Experience
    exp_pattern = r"(<!-- PORTFOLIO_EXPERIENCE_START -->).*?(<!-- PORTFOLIO_EXPERIENCE_END -->)"
    content = re.sub(exp_pattern, rf"\1\n{exp_html}\n                    \2", content, flags=re.DOTALL)
    
    # Replace Credentials
    cred_pattern = r"(<!-- PORTFOLIO_CREDENTIALS_START -->).*?(<!-- PORTFOLIO_CREDENTIALS_END -->)"
    content = re.sub(cred_pattern, rf"\1\n{edu_html}\n                    \2", content, flags=re.DOTALL)
    
    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Portfolio HTML rendered idempotently.")

if __name__ == "__main__":
    build_portfolio_html()
