import asyncio
from playwright.async_api import async_playwright
import os
import math
from PIL import Image, ImageChops

async def capture_and_compare():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1200, 'height': 800}, device_scale_factor=1)
        
        # 1. Manual CV
        man_path = os.path.abspath('mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.html')
        await page.goto(f'file:///{man_path}', wait_until='networkidle')
        h_man = await page.evaluate('document.documentElement.scrollHeight')
        await page.set_viewport_size({'width': 1200, 'height': h_man})
        await page.screenshot(path='artifacts/manual_cv_fresh.png', full_page=True)
        
        # 2. Generated CV
        gen_path = os.path.abspath('compiled_assets/CV_Master.html')
        await page.goto(f'file:///{gen_path}', wait_until='networkidle')
        h_gen = await page.evaluate('document.documentElement.scrollHeight')
        await page.set_viewport_size({'width': 1200, 'height': h_gen})
        await page.screenshot(path='artifacts/generated_cv_fresh.png', full_page=True)
        
        await browser.close()
        
        print(f"Manual Height: {h_man}")
        print(f"Generated Height: {h_gen}")
        
        if h_man != h_gen:
            print("Dimensions are not identical.")
        else:
            print("Dimensions are identical.")
            
        img1 = Image.open('artifacts/manual_cv_fresh.png')
        img2 = Image.open('artifacts/generated_cv_fresh.png')
        
        # Ensure identical sizes for comparison
        if img1.size != img2.size:
            print("Cannot compute pixel diff because dimensions differ.")
        else:
            diff = ImageChops.difference(img1, img2)
            bbox = diff.getbbox()
            if bbox:
                print(f"Diff Bounding Box: {bbox}")
                # Very rough percentage
                diff_data = diff.getdata()
                non_zero = sum(1 for p in diff_data if p != (0,0,0,0) and p != (0,0,0) and p != 0)
                total = img1.size[0] * img1.size[1]
                print(f"Pixel Diff %: {(non_zero / total) * 100:.2f}%")
            else:
                print("Pixel Diff %: 0.00% (Identical)")

asyncio.run(capture_and_compare())
