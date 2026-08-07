import { test, expect } from '@playwright/test';
import path from 'path';

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

    // Check visibility of some key certificate cards
    const pgceCard = page.locator('div[data-cert-id="pgce"]');
    await expect(pgceCard).toBeVisible();

    const bedCard = page.locator('div[data-cert-id="bed"]');
    await expect(bedCard).toBeVisible();

    const tesolCard = page.locator('div[data-cert-id="tesol"]');
    await expect(tesolCard).toBeVisible();

});
