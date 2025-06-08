import { test, expect } from '@playwright/test';

const baseURL = 'http://127.0.0.1:8000';

// Authentication Tests
test('Login Page Loads', async ({ page }) => {
  // Go to login page and expect there to be a form
  await page.goto(`${baseURL}/login`);
  await expect(page.locator('form')).toBeVisible();
});

test('Invalid Login Attempt', async ({ page }) => {
  // Go to login page and enter invalid details, click login and expect there to be a flash message
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'asdf');
  await page.fill('input[name = "password"]', 'asdf');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('Invalid username or password.');
});

test('Valid Login Attempt', async ({ page }) => {
  // Go to the login page and login as admin and expect there to a flash message
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('Logged in successfully.');
});

test('Invalid Signup Attempt', async ({ page }) => {
  // Go to the signup page and leave username field empty and expect there to be a flash message
  await page.goto(`${baseURL}/signup`);
  await page.fill('input[name = "username"]', '');
  await page.fill('input[name = "password"]', '123');
  await page.getByRole('button', { name: 'Sign up' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('Invalid username or password field.');
});

test('Valid Signup Attempt', async ({ page }) => {
  // Sign up using valid credentials and expect there to be a flash message
  await page.goto(`${baseURL}/signup`);
  await page.fill('input[name = "username"]', 'test');
  await page.fill('input[name = "password"]', 'test');
  await page.getByRole('button', { name: 'Sign up' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('Account created.');
});

// Photo Functionality Tests
test('Invalid Upload Attempt', async ({ page }) => {
  // Login as admin
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  // Go to upload page and leave fields empty, there should be a flash message
  await page.goto(`${baseURL}/upload`);
  await page.getByRole('button', { name: 'Upload' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('User, Caption and Description fields cannot be left empty.');

  // Upload a photo with valid fields but no photo, there should be a flash message
  await page.fill('input[name = "name"]', 'test');
  await page.fill('input[name = "caption"]', 'caption');
  await page.fill('textarea[name = "description"]', 'description');
  await page.getByRole('button', { name: 'Upload' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('No file selected!');
});

test('Valid Upload Attempt', async ({ page }) => {
  // Login as admin
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  // Upload the file from ./assets with valid fields
  await page.goto(`${baseURL}/upload`);
  await page.setInputFiles('input[type = "file"]', 'project/tests/assets/sample.jpg');
  await page.fill('input[name = "name"]', 'test');
  await page.fill('input[name = "caption"]', 'caption');
  await page.fill('textarea[name = "description"]', 'description');
  await page.getByRole('button', { name: 'Upload' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('New Photo Successfully Created');
});

test('Invalid Edit Photo Attempt', async ({ page }) => {
  // Login as admin
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  // Try edit a non-existant photo
  await page.goto(`${baseURL}/photo/999/edit/`);
  await expect(page.locator('body')).toContainText('Not Found');
});

test('Valid Photo Edit Attempt', async ({ page }) => {
  //Login as admin
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  //Attempt to edit photo with id 10 and valid fields
  await page.goto(`${baseURL}/photo/10/edit/`);
  await page.fill('textarea[name = "description"]', 'description');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('Photo Successfully Edited');
});

test('Delete Photo Attempt', async ({ page }) => {
  // Login as admin
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  // Find the delete links and click on the first one i.e. delete the first photo
  const deleteLinks = await page.locator('a[title = "Delete this photo"]').all();
  if (deleteLinks.length > 0) {
    await deleteLinks[0].click();
    await expect(page.locator('.flash-message.message')).toContainText('Successfully Deleted');
  }
});

// Admin Functionality Tests
test('Admin Privileges', async ({ page }) => {
  // Login as admin
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  // Should be able to see admin panel page
  await page.goto(`${baseURL}/admin/users/`);
  await expect(page.locator('h2')).toContainText('Manage Users');
});

test('Admin Panel User Promote/Delete', async ({ page }) => {
  // Credentials for a dummy user
  const dummyUsername = 'dummy';
  const dummyPassword = 'dummy';

  // Sign up the dummy user
  await page.goto(`${baseURL}/signup`);
  await page.fill('input[name = "username"]', dummyUsername);
  await page.fill('input[name = "password"]', dummyPassword);
  await page.getByRole('button', { name: 'Sign Up' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('Account created');

  // Login as admin
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  // Go to the admin panel
  await page.goto(`${baseURL}/admin/users`);
  const userRow = page.locator('tbody tr').filter({has: page.locator('td:nth-child(2)', { hasText: 'dummy' })});
  await expect(userRow.locator('td:nth-child(3)')).toHaveText('No');

  // Give the dummy user admin priveleges
  await userRow.getByRole('button', { name: 'Promote' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('User Access Successfully Modified');

  // Refresh the page and expect the field for the dummy user admin priveleges to be yes
  await page.goto(`${baseURL}/admin/users`);
  await expect(userRow.locator('td:nth-child(3)')).toHaveText('Yes');

  // Log out from admin account
  await page.goto(`${baseURL}/logout`);

  // Log in as dummy user
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', dummyUsername);
  await page.fill('input[name = "password"]', dummyPassword);
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL(`${baseURL}/`);

  // Access the admin panel as dummy user (now promoted)
  await page.goto(`${baseURL}/admin/users`);
  await expect(userRow.locator('td:nth-child(3)')).toHaveText('Yes');

  // Log out from dummy account and log in as admin
  await page.goto(`${baseURL}/logout`);
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  // Delete the dummy user
  await page.goto(`${baseURL}/admin/users`);
  await userRow.getByRole('button', { name: 'Delete' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('User Access Successfully Modified');

  // Try logging in as dummy user
  await page.goto(`${baseURL}/logout`);
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', dummyUsername);
  await page.fill('input[name = "password"]', dummyPassword);
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.locator('.flash-message.message')).toContainText('Invalid username or password.');
});

// Favourites Functionality Tests
test('Favourites Functionality', async ({ page }) => {
  //Log in as admin
  await page.goto(`${baseURL}/login`);
  await page.fill('input[name = "username"]', 'admin');
  await page.fill('input[name = "password"]', 'admin');
  await page.getByRole('button', { name: 'Login' }).click();

  // Get an array of all the favourite buttons and click on the first one, then visit the favourites page where it should show up
  const favButtons = await page.locator('form[action*="/favourite"] button').all();
  if (favButtons.length > 0) {
    await favButtons[0].click();
    await page.goto(`${baseURL}/favourites`);
    await expect(page.locator('.image-box')).toBeVisible();
  }
});

test('SQL Injection on Login', async ({ page }) => {
  // Go to login page
  await page.goto(`${baseURL}/login`);

  // Input SQL injection for login credentials
  await page.fill('input[name="username"]', `' OR '1'='1`);
  await page.fill('input[name="password"]', 'any');
  await page.getByRole('button', { name: 'Login' }).click();

  // Expected output is a flash message
  await expect(page.locator('.flash-message.message')).toContainText('Invalid username or password.');
});

test('SQL Injection on Sign Up', async ({ page }) => {
  // Go to signup page
  await page.goto(`${baseURL}/signup`);

  // Sign up with SQL injection credentials
  await page.fill('input[name="username"]', `' OR '1'='1`);
  await page.fill('input[name="password"]', 'any');
  await page.getByRole('button', { name: 'Sign Up' }).click();

  // Account should be created given that the input will be sanitised
  await expect(page.locator('.flash-message.message')).toContainText('Account created.');

  // Go to login page
  await page.goto(`${baseURL}/login`);

  // Input the same credentials
  await page.fill('input[name="username"]', `' OR '1'='1`);
  await page.fill('input[name="password"]', 'any');
  await page.getByRole('button', { name: 'Login' }).click();

  // User should be logged in given that the inputs will be filtered the same way again
  await expect(page.locator('.flash-message.message')).toContainText('Logged in successfully.');
});