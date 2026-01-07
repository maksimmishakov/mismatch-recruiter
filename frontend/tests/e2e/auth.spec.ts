import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should register new user', async ({ page }) => {
    await page.goto('/register');
    await page.fill('input[name=email]', 'newuser@example.com');
    await page.fill('input[name=password]', 'password123');
    await page.fill('input[name=name]', 'Test User');
    await page.click('button:has-text("Register")');
    
    await expect(page).toHaveURL('/dashboard');
  });

  test('should login user', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name=email]', 'test@example.com');
    await page.fill('input[name=password]', 'password123');
    await page.click('button:has-text("Login")');
    
    await expect(page).toHaveURL('/dashboard');
  });
});
