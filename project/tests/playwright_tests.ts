import { test, expect } from '@playwright/test';

test('login and upload photo', async ({ page }) => {
  await page.goto('http://localhost:8000/login');

  await page.fill('input[name="username"]', 'admin');
  await page.fill('input[name="password"]', 'adminpass');
  await page.click('text=Login');

  await expect(page).toHaveURL('http://localhost:8000/');

  await page.goto('http://localhost:8000/upload/');
  const fileInput = await page.$('input[type="file"]');
  if(fileInput){
    await fileInput.setInputFiles('tests/assets/sample.jpg');
  }
  else{
    throw new Error("sample.jpeg not found");
  }
  
  await page.fill('input[name="caption"]', 'Test Image');
  await page.fill('textarea[name="description"]', 'Test Description');
  await page.click('text=Upload');

  await expect(page.locator('.flash')).toHaveText('New Photo admin Successfully Created');
});
