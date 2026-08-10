import asyncio
from playwright.async_api import async_playwright
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

async def get_geometry(page):
    return await page.evaluate('''() => {
        const result = [];
        const elements = document.querySelectorAll('body, section, div, h1, h2, h3, p, ul, li, span');
        elements.forEach(el => {
            if (el.tagName.toLowerCase() === 'script' || el.tagName.toLowerCase() === 'style' || el.tagName.toLowerCase() === 'link') return;
            
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 && rect.height === 0) return;
            
            const style = window.getComputedStyle(el);
            let text = el.innerText ? el.innerText.trim() : '';
            if (text.length > 50) text = text.substring(0, 50) + '...';
            
            result.push({
                tag: el.tagName.toLowerCase(),
                className: el.className,
                id: el.id,
                text: text,
                rect: {
                    top: rect.top,
                    left: rect.left,
                    width: rect.width,
                    height: rect.height
                },
                style: {
                    marginTop: style.marginTop,
                    marginBottom: style.marginBottom,
                    paddingTop: style.paddingTop,
                    paddingBottom: style.paddingBottom,
                    lineHeight: style.lineHeight,
                    fontSize: style.fontSize,
                    display: style.display,
                    position: style.position
                }
            });
        });
        return result;
    }''')

async def main():
    manual = BASE_DIR / 'mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.html'
    gen = BASE_DIR / 'compiled_assets/CV_Master.html'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel="msedge")
        
        page = await browser.new_page()
        await page.goto(f'file:///{manual.absolute()}')
        man_data = await get_geometry(page)
        
        await page.goto(f'file:///{gen.absolute()}')
        gen_data = await get_geometry(page)
        
        await browser.close()
        
    (BASE_DIR / 'manual_geometry.json').write_text(json.dumps(man_data, indent=2), encoding='utf-8')
    (BASE_DIR / 'gen_geometry.json').write_text(json.dumps(gen_data, indent=2), encoding='utf-8')
    print("Geometry extracted.")

asyncio.run(main())
