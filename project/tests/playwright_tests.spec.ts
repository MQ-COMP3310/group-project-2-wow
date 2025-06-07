import { test, expect } from '@playwright/test';

test('login and upload photo', async ({ page }) => {
  await page.goto('http://localhost:8000/login');

  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'adminpass');
  await page.click('text=Login');

  await expect(page).toHaveURL('http://localhost:8000/');


});
