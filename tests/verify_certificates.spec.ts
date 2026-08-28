import { test, expect } from '@playwright/test';
import path from 'path';
import fs from 'fs';

test('Certificate images load without 404s', async ({ page }) => {
    const htmlPath = path.resolve(__dirname, '../mo-portfolio-v2/index.html');
    const fileUrl = `file:///${htmlPath.replace(/\\/g, '/')}`;

    const failedRequests = [];

    page.on('response', response => {
        if (response.status() >= 400 && response.request().resourceType() === 'image') {
            failedRequests.push({
                url: response.url(),
                status: response.status()
            });
        }
    });

    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    // Assert that we had no failed image requests
    expect(failedRequests).toEqual([]);

    // Derive expected credential IDs from the view model. The canonical
    // education IDs in career-data/facts/education.yml are uppercased (e.g.
    // QUAL-3002); the rendered DOM projects them to lowercase (qual-3002).
    const vmPath = path.resolve(__dirname, '../artifacts/cv_view_models/portfolio.json');
    const vm = JSON.parse(fs.readFileSync(vmPath, 'utf8'));
    const publicQuals = (vm.qualifications || [])
        .filter((q: any) => q.entity_type === 'qualification')
        .map((q: any) => String(q.id).toLowerCase());

    // The contract: every publicly rendered qualification must have a visible
    // card whose data-cert-id equals the lowercase canonical ID.
    expect(publicQuals.length).toBeGreaterThan(0);
    for (const certId of publicQuals) {
        const card = page.locator(`div[data-cert-id="${certId}"]`);
        await expect(card).toBeVisible();
    }
});
