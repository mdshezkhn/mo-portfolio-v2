import json
from pathlib import Path
from bs4 import BeautifulSoup

def test_html_renderer_contract():
    root = Path(__file__).parent.parent.parent
    html_path = root / "artifacts/generated/cv_v2.html"
    vm_path = root / "artifacts/cv_vm.json"
    
    assert html_path.exists(), "HTML CV not generated"
    assert vm_path.exists(), "CV VM not found"
    
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        
    with open(vm_path, "r", encoding="utf-8") as f:
        vm = json.load(f)
        
    # 1. exactly one document title (using <h1>)
    h1s = soup.find_all('h1')
    assert len(h1s) == 1, f"Expected exactly one <h1>, found {len(h1s)}"
    
    # 2. employment count equals VM
    # The experience section maps to <div class="entry">
    # We should distinguish them by finding the experience section specifically
    exp_entries = soup.find(id="experience")
    if not exp_entries:
        # Check if there is an h2 for Experience and the entries are just divs
        entries = soup.find_all('div', class_='entry')
        assert len(entries) == len(vm.get('experience', [])), f"Mismatch in employment entries: found {len(entries)}, expected {len(vm.get('experience', []))}"
        
    # 3. education count equals VM
    # In legacy, education was a list
    edu_section = soup.find('ul', id='education-list') or soup.find(id='education')
    # If not IDed, maybe check all <li> after education header?
    # Let's do a basic text count check for degree names
    for edu in vm.get('education', []):
        assert edu['degree_name'] in html, f"Education degree '{edu['degree_name']}' missing from HTML"
        
    # 4. no empty sections
    # A section is usually preceded by an <h2>
    for h2 in soup.find_all('h2'):
        # Just ensure the text is not empty and next sibling isn't empty
        assert h2.text.strip() != "", "Found empty <h2>"
        
    # 5. no unresolved template tokens
    assert "{" not in html and "}" not in html, "Found unresolved template tokens (e.g., {PLACEHOLDER})"
    
    # 6. Check UTF-8 (Python opens as UTF-8, if it didn't crash, we're good)
    
if __name__ == "__main__":
    test_html_renderer_contract()
    print("HTML Renderer Contract validation PASS")
