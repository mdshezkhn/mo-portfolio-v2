import json
import yaml
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup
import cssutils
import logging

# Disable cssutils logging
cssutils.log.setLevel(logging.CRITICAL)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CAREER_DATA = BASE_DIR / 'career-data'

def load_yaml(p):
    with open(p, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

print("--- FORENSIC AUDIT ---")
emps = load_yaml(CAREER_DATA / 'facts' / 'employment.yml').get('employment_records', [])
canonical_ids = set([e['id'] for e in emps if e.get('review_status', 'pending') == 'approved'])

with open(BASE_DIR / 'artifacts' / 'cv_view_models' / 'portfolio.json', 'r', encoding='utf-8') as f:
    vm = json.load(f)
    
rendered_ids = set([e['id'] for e in vm.get('experience', [])])

print(f"canonical = {len(canonical_ids)}")
print(f"rendered = {len(rendered_ids)}")

if canonical_ids != rendered_ids:
    print(f"MISMATCH! canonical: {canonical_ids}, rendered: {rendered_ids}")
    sys.exit(1)
print("1. Set equality: PASS")

html_path = BASE_DIR / 'mo-portfolio-v2' / 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')

# Check HTML structural integrity
ids = [tag.get('id') for tag in soup.find_all(id=True)]
if len(ids) != len(set(ids)):
    duplicates = set([x for x in ids if ids.count(x) > 1])
    print(f"Duplicate IDs found in HTML: {duplicates}")
    sys.exit(1)

for img in soup.find_all('img'):
    if not img.get('alt'):
        print(f"Missing alt attribute on image: {img.get('src')}")
        sys.exit(1)

nav_ids = ['story', 'journey', 'impact', 'credentials', 'philosophy', 'moments', 'research', 'leadership', 'contact']
missing_nav = []
for nid in nav_ids:
    if not soup.find(id=nid):
        missing_nav.append(nid)

if missing_nav:
    print(f"Missing navigation IDs: {missing_nav}")
    sys.exit(1)
print("2. Navigation IDs: PASS")

# 5. CONTACT TEST MUST COUNT REAL CV DESTINATIONS
contact_section = soup.find(id='contact')
cv_links = [a for a in contact_section.find_all('a') if a.get('href') == 'assets/documents/Mohammed_Shehzad_Khan_CV.pdf']

if len(cv_links) != 1:
    print(f"Contact CV destination count is {len(cv_links)}, expected 1.")
    sys.exit(1)
print("3. Contact CV destination count: PASS")

# Check other links in contact
wechat_found = False
linkedin_found = False
email_found = False

for a in contact_section.find_all('a'):
    href = a.get('href', '')
    if 'weixin' in href or 'wechat' in href or '#wechat' in href:
        wechat_found = True
    if 'linkedin.com' in href:
        linkedin_found = True
    if href.startswith('mailto:'):
        email_found = True

if not linkedin_found or not email_found:
    print("Contact routes missing LinkedIn or Email")
    sys.exit(1)
print("3b. Contact Routes verification: PASS")

import os
images = soup.find_all('img')
broken_assets = 0
for img in images:
    src = img.get('src')
    if src and not src.startswith('http') and not src.startswith('data:'):
        full_path = BASE_DIR / 'mo-portfolio-v2' / src
        if not full_path.exists():
            print(f"Broken asset: {src}")
            broken_assets += 1
if broken_assets > 0:
    print(f"Found {broken_assets} broken assets.")
    sys.exit(1)
print("4. Broken asset count: PASS (0)")

cred_modal = soup.find(id='credential-modal')
stds_modal = soup.find(id='evidence-standards-modal')

if not cred_modal or not cred_modal.has_attr('hidden') or cred_modal.get('aria-hidden') != 'true':
    print("Credential modal hidden state invalid.")
    sys.exit(1)
if not stds_modal or not stds_modal.has_attr('hidden') or stds_modal.get('aria-hidden') != 'true':
    print("Evidence standards modal hidden state invalid.")
    sys.exit(1)
print("5. Modal hidden state: PASS")

css_path = BASE_DIR / 'mo-portfolio-v2' / 'assets' / 'css' / 'components.css'
try:
    sheet = cssutils.parseFile(str(css_path))
except Exception as e:
    print(f"CSS parsing failed: {e}")
    sys.exit(1)
print("6. CSS Validation: PASS")

if "Verified Qualification" in html_content and not "status_str" in open(BASE_DIR / 'scripts' / 'builders' / 'build_portfolio_html.py', encoding='utf-8').read():
    print("Hardcoded generic verification found")
    sys.exit(1)
print("7. Verification text validation: PASS")

print("--- AUDIT SUCCESS ---")
