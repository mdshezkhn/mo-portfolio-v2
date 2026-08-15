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
    # Render responsibilities (role scope) - always shown
    if exp.get("responsibilities"):
        html += """                                    <div class="tl-responsibilities">
                                        <h4 class="tl-section-title">Role Scope</h4>
                                        <ul class="tl-bullets tl-responsibility-list">
"""
        for resp in exp["responsibilities"]:
            html += f"                                            <li class=\"tl-responsibility\">{resp}</li>\n"
        html += """                                        </ul>
                                    </div>
"""
    # Render verified achievements (evidence-backed claims) - only when verified
    if exp.get("bullets"):
        html += """                                    <div class="tl-achievements">
                                        <h4 class="tl-section-title">Verified Highlights</h4>
                                        <ul class="tl-bullets tl-achievement-list">
"""
        for b in exp["bullets"]:
            html += f"                                            <li class=\"tl-achievement\">{b}</li>\n"
        html += """                                        </ul>
                                    </div>
"""
    
    html += """                                </div>
                            </div>
                        </div>
                    </div>"""
    return html

def render_qualification(qual):
    cert_id = qual['id'].lower()
    status_str = qual.get('status', 'Verified Qualification')
    html = f"""
                    <div class="edu-card" data-cert-id="{cert_id}" data-title="{qual['degree']}" data-issuer="{qual['institution']}" data-status="{status_str}">
                        <div class="cert-thumb">
                            <span class="cert-thumb-overlay">🔍 View document</span>
                        </div>
                        <h4 class="edu-title">{qual['degree']}</h4>
                        <p class="edu-sch">{qual['institution']}</p>
                        <time class="edu-yr">{qual['date']}</time>
                        <div class="verification-panel">
                            <span class="v-badge">✓ {status_str}</span>
                            <div class="v-details">Officially verified by provenance engine.</div>
                        </div>
                    </div>"""
    return html

def render_certification(qual):
    cert_id = qual['id'].lower()
    status_str = qual.get('status', 'Verified Certification')
    html = f"""
                    <div class="cert-card" data-cert-id="{cert_id}" data-title="{qual['degree']}" data-issuer="{qual['institution']}" data-status="{status_str}">
                        <div class="cert-thumb">
                            <span class="cert-thumb-overlay">🔍 View document</span>
                        </div>
                        <h4 class="cert-title">{qual['degree']}</h4>
                        <p class="cert-org">{qual['institution']}</p>
                        <div class="verification-panel">
                            <span class="v-badge">✓ {status_str}</span>
                            <div class="v-details">Officially verified by provenance engine.</div>
                        </div>
                    </div>"""
    return html

def render_cpd(qual):
    html = f"""
                      <div class="pd-card">
                          <h4>{qual['degree']}</h4>
                          <p>{qual['institution']}</p>
                      </div>"""
    return html

def build_portfolio_html():
    if not PORTFOLIO_VM_PATH.exists():
        print("Portfolio View Model not found. Did the build_domain_model.py run?")
        return
        
    with open(PORTFOLIO_VM_PATH, "r", encoding="utf-8") as f:
        vm = json.load(f)
        
    exp_html = "\n".join([render_experience(e) for e in vm.get("experience", [])])
    
    edu_quals = [q for q in vm.get("qualifications", []) if q.get("entity_type") in ("qualification", "institution")]
    cert_quals = [q for q in vm.get("qualifications", []) if q.get("entity_type") == "certification"]
    cpd_quals = [q for q in vm.get("qualifications", []) if q.get("entity_type") == "professional_development"]
    
    cred_html = ""
    
    if edu_quals:
        cred_html += '                  <h3 class="subsection-title">Education</h3>\n'
        cred_html += '                  <div id="edu-grid-container" class="edu-grid">\n'
        cred_html += "\n".join([render_qualification(q) for q in edu_quals])
        cred_html += '\n                  </div>\n'
        
    if cert_quals:
        cred_html += '                  <h3 class="subsection-title">Professional Qualifications &amp; Development</h3>\n'
        cred_html += '                  <div id="prof-grid-container" class="certs-grid">\n'
        cred_html += "\n".join([render_certification(q) for q in cert_quals])
        cred_html += '\n                  </div>\n'
        
    if cpd_quals:
        cred_html += '                  <h3 class="subsection-title">Continuing Professional Development</h3>\n'
        cred_html += '                  <div class="pd-grid">\n'
        cred_html += "\n".join([render_cpd(q) for q in cpd_quals])
        cred_html += '\n                  </div>\n'
    
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace Experience
    exp_pattern = r"(<!-- PORTFOLIO_EXPERIENCE_START -->).*?(<!-- PORTFOLIO_EXPERIENCE_END -->)"
    content = re.sub(exp_pattern, rf"\1\n{exp_html}\n                    \2", content, flags=re.DOTALL)
    
    # Replace Credentials
    cred_pattern = r"(<!-- PORTFOLIO_CREDENTIALS_START -->).*?(<!-- PORTFOLIO_CREDENTIALS_END -->)"
    content = re.sub(cred_pattern, rf"\1\n{cred_html}\n                    \2", content, flags=re.DOTALL)
    
    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Portfolio HTML rendered idempotently.")

if __name__ == "__main__":
    build_portfolio_html()
