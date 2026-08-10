import sys
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import subprocess
import os
import hashlib

BASE_DIR = Path(__file__).parent.parent.parent
ARTIFACTS_DIR = Path('C:/Users/Mohammed Shehzad/.gemini/antigravity-ide/brain/43da049a-d50c-4200-b819-a34b35097da2')

def get_image_difference(img1_path, img2_path):
    if not img1_path.exists() or not img2_path.exists():
        return "Images not found"
        
    try:
        im1 = Image.open(img1_path).convert('RGB')
        im2 = Image.open(img2_path).convert('RGB')
    except Exception as e:
        return f"Pillow missing or load error: {e}"
        
    if im1.size != im2.size:
        return f"Size mismatch: {im1.size} vs {im2.size}"
        
    diff = ImageChops.difference(im1, im2)
    stat = ImageStat.Stat(diff)
    diff_percent = sum(stat.mean) / (255.0 * 3) * 100
    return f"{diff_percent:.2f}% pixel difference"

print("=== 1. VISUAL EQUIVALENCE ===")
print(get_image_difference(ARTIFACTS_DIR / 'manual_cv.png', ARTIFACTS_DIR / 'generated_cv.png'))

print("\n=== 2. SEMANTIC DOM COMPARISON ===")
manual = BASE_DIR / 'mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.html'
gen = BASE_DIR / 'compiled_assets/CV_Master.html'
sm = BeautifulSoup(manual.read_text(encoding='utf-8'), 'html.parser')
sg = BeautifulSoup(gen.read_text(encoding='utf-8'), 'html.parser')

print(f"Manual Title: {sm.title.string if sm.title else None}")
print(f"Gen Title: {sg.title.string if sg.title else None}")

# Check privacy scan (raw phone number)
gen_text = sg.get_text()
if '+86' in gen_text or '187' in gen_text: # partial match for the number
    print("Privacy: FAILED - Raw phone number found")
else:
    print("Privacy: PASS - Raw phone number omitted")

if "Phone provided on PDF download" in gen_text:
    print("Privacy: PASS - Presentation text found")
else:
    print("Privacy: FAILED - Presentation text missing")

print("\n=== 3. GIT STATUS HYGIENE ===")
subprocess.run("git status --short", shell=True)
