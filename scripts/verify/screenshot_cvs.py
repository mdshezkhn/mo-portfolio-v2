import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
manual = BASE_DIR / 'mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.html'
gen = BASE_DIR / 'compiled_assets/CV_Master.html'
ARTIFACTS_DIR = Path('C:/Users/Mohammed Shehzad/.gemini/antigravity-ide/brain/43da049a-d50c-4200-b819-a34b35097da2')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel="msedge")
        page = await browser.new_page()
        
        await page.goto(f'file:///{manual.absolute()}')
        await page.screenshot(path=str(ARTIFACTS_DIR / 'manual_cv.png'), full_page=True)
        
        await page.goto(f'file:///{gen.absolute()}')
        await page.screenshot(path=str(ARTIFACTS_DIR / 'generated_cv.png'), full_page=True)
        
        await browser.close()

asyncio.run(main())
