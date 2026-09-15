import { chromium } from 'playwright-core';

const exe = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const url  = 'file:///C:/Users/Mohammed%20Shehzad/Documents/Mo%20Digital%20Portfolio/mo-portfolio-v2/index.html';

const viewports = [
    { name: 'desktop', width: 1440, height: 900 },
    { name: 'tablet',  width: 768,  height: 1024 },
    { name: 'mobile',  width: 390,  height: 844 },
    { name: 'small',   width: 320,  height: 800 },
];

(async () => {
    const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
    const results = [];

    for (const vp of viewports) {
        const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
        const page = await context.newPage();
        const errors = [];
        page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
        page.on('pageerror', err => errors.push(err.message));

        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(2500);

        const sections = await page.evaluate(() => {
            return [...document.querySelectorAll('section[id]')].map(s => ({
                id: s.id,
                text: s.textContent.trim().slice(0, 60),
                visible: !!(s.offsetWidth || s.offsetHeight),
                opacity: getComputedStyle(s).opacity,
            }));
        });

        const brokenImages = await page.evaluate(() =>
            [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src)
        );

        const horizontalScroll = await page.evaluate(() => {
    if (document.documentElement.scrollWidth <= document.documentElement.clientWidth) return false;
    const bad = [];
    document.querySelectorAll('*').forEach(el => {
        if (el.scrollWidth > document.documentElement.clientWidth + 1) {
            bad.push({ tag: el.tagName, cls: el.className && el.className.baseVal === undefined ? String(el.className).slice(0, 80) : '', id: el.id });
        }
    });
    return bad.slice(0, 10);
});

        results.push({ viewport: vp.name, width: vp.width, sections, brokenImages, horizontalScroll, errors });
        await page.close();
    }

    await browser.close();
    console.log(JSON.stringify(results, null, 2));
})();
