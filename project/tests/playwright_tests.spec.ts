import { test, expect } from '@playwright/test';

test('login page loads correctly', async ({ page }) => {
  await page.goto('http://127.0.0.1:8000/login');
  await expect(page.locator('form')).toBeVisible();
});