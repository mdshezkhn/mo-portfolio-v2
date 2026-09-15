#!/usr/bin/env python3
"""
Generate CV PDF from cv.html using Puppeteer.
Run from the repository root.

Usage:
    python assets/documents/generate_pdf.py

Requires:
    pip install puppeteer
    or: npm install -g puppeteer-cli
"""

import subprocess
import sys
from pathlib import Path

CV_HTML = Path("mo-portfolio-v2/assets/documents/cv/cv.html")
CV_PDF = Path("mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.pdf")

def main():
    if not CV_HTML.exists():
        print(f"Error: CV HTML not found at {CV_HTML}")
        sys.exit(1)

    # Method 1: Try playwright
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            html_path = CV_HTML.resolve()
            page.goto(f"file:///{html_path}")
            page.pdf(path=str(CV_PDF), format="A4", print_background=True)
            browser.close()
        print(f"PDF generated successfully: {CV_PDF}")
        return
    except ImportError:
        print("playwright not installed, trying puppeteer...")

    # Method 2: Try puppeteer via npx
    result = subprocess.run(
        ["npx", "puppeteer-cli", str(CV_HTML.resolve()), str(CV_PDF.resolve())],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"PDF generated successfully: {CV_PDF}")
        return

    print("Could not generate PDF.")
    print("Install playwright: pip install playwright && playwright install chromium")
    print("Or use puppeteer: npm install -g puppeteer-cli")
    sys.exit(1)

if __name__ == "__main__":
    main()