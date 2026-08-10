import os
import sys
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).parent.parent.parent

def run_verifier():
    result = subprocess.run(["python", str(BASE_DIR / "scripts" / "verify" / "verify_build.py"), "--no-build"], capture_output=True, text=True)
    return result.returncode

def test_negative(description, setup, teardown):
    print(f"Negative Test: {description}...", end=" ")
    setup()
    code = run_verifier()
    teardown()
    if code != 0:
        print("PASS (caught)")
        return True
    else:
        print("FAIL (uncaught)")
        return False

# Tests to run
def test_missing_css_class():
    html_path = BASE_DIR / 'compiled_assets' / 'CV_Master.html'
    backup = html_path.read_text(encoding='utf-8')
    def setup():
        html_path.write_text(backup.replace('class="entry"', 'class="entry-broken"'), encoding='utf-8')
    def teardown():
        html_path.write_text(backup, encoding='utf-8')
    return test_negative("Missing CSS class", setup, teardown)

def test_missing_employer():
    html_path = BASE_DIR / 'compiled_assets' / 'CV_Master.html'
    backup = html_path.read_text(encoding='utf-8')
    def setup():
        html_path.write_text(backup.replace('Aoxin', 'MissingOrg'), encoding='utf-8')
    def teardown():
        html_path.write_text(backup, encoding='utf-8')
    return test_negative("Missing Employer Name", setup, teardown)

def main():
    print("Running Negative Verification Tests...")
    success = test_missing_css_class() and test_missing_employer()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
