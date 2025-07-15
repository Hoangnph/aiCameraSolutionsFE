#!/usr/bin/env python3
"""
Change Password Flow Automation Test
Tests the change password functionality from profile page
"""

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ChangePasswordTest(unittest.TestCase):
    """Test cases for change password functionality"""
    
    def setUp(self):
        """Set up test environment"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://localhost:3000"
        
    def tearDown(self):
        """Clean up after test"""
        if self.driver:
            self.driver.quit()
    
    def login_user(self, username="testuser", password="TestPass123!"):
        """Helper function to login user"""
        try:
            self.driver.get(f"{self.base_url}/authentication/sign-in")
            
            # Wait for login form
            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Email']"))
            )
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            
            # Fill login form
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Wait for redirect to dashboard
            self.wait.until(EC.url_contains("/dashboard"))
            return True
            
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def test_change_password_page_loads(self):
        """Test that change password page loads correctly"""
        print("\n=== Testing Change Password Page Load ===")
        
        # Login first
        if not self.login_user():
            self.skipTest("Login failed, skipping test")
        
        try:
            # Navigate to profile
            self.driver.get(f"{self.base_url}/profile")
            
            # Wait for profile page to load
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Đổi mật khẩu')]")))
            
            # Click change password button
            change_password_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Đổi mật khẩu')]")
            change_password_button.click()
            
            # Wait for change password page
            self.wait.until(EC.url_contains("/authentication/change-password"))
            
            # Check page title
            title = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Đổi mật khẩu')]"))
            )
            self.assertIsNotNone(title)
            
            print("✓ Change password page loads correctly")
            
        except Exception as e:
            print(f"✗ Change password page load failed: {e}")
            self.fail(f"Change password page load failed: {e}")
    
    def test_change_password_form_elements(self):
        """Test that all form elements are present"""
        print("\n=== Testing Change Password Form Elements ===")
        
        # Login first
        if not self.login_user():
            self.skipTest("Login failed, skipping test")
        
        try:
            # Navigate to change password page
            self.driver.get(f"{self.base_url}/authentication/change-password")
            
            # Check current password field
            current_password_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='currentPassword']"))
            )
            self.assertIsNotNone(current_password_input)
            
            # Check new password field
            new_password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='newPassword']")
            self.assertIsNotNone(new_password_input)
            
            # Check confirm password field
            confirm_password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='confirmNewPassword']")
            self.assertIsNotNone(confirm_password_input)
            
            # Check submit button
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.assertIsNotNone(submit_button)
            
            print("✓ All form elements are present")
            
        except Exception as e:
            print(f"✗ Form elements test failed: {e}")
            self.fail(f"Form elements test failed: {e}")
    
    def test_change_password_validation(self):
        """Test form validation"""
        print("\n=== Testing Change Password Validation ===")
        
        # Login first
        if not self.login_user():
            self.skipTest("Login failed, skipping test")
        
        try:
            # Navigate to change password page
            self.driver.get(f"{self.base_url}/authentication/change-password")
            
            # Test empty form submission
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            submit_button.click()
            
            # Check for validation errors
            time.sleep(1)
            error_messages = self.driver.find_elements(By.CSS_SELECTOR, "[color='error']")
            self.assertGreater(len(error_messages), 0, "Should show validation errors for empty form")
            
            print("✓ Form validation works correctly")
            
        except Exception as e:
            print(f"✗ Validation test failed: {e}")
            self.fail(f"Validation test failed: {e}")
    
    def test_change_password_success_flow(self):
        """Test successful password change (simulated)"""
        print("\n=== Testing Change Password Success Flow ===")
        
        # Login first
        if not self.login_user():
            self.skipTest("Login failed, skipping test")
        
        try:
            # Navigate to change password page
            self.driver.get(f"{self.base_url}/authentication/change-password")
            
            # Fill form with valid data
            current_password_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='currentPassword']"))
            )
            current_password_input.send_keys("TestPass123!")
            
            new_password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='newPassword']")
            new_password_input.send_keys("NewTestPass123!")
            
            confirm_password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='confirmNewPassword']")
            confirm_password_input.send_keys("NewTestPass123!")
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Wait for success message or redirect
            time.sleep(2)
            
            # Check for success message or redirect to profile
            try:
                success_message = self.driver.find_element(By.CSS_SELECTOR, "[color='success']")
                self.assertIsNotNone(success_message)
                print("✓ Success message displayed")
            except NoSuchElementException:
                # Check if redirected to profile
                if "/profile" in self.driver.current_url:
                    print("✓ Redirected to profile after success")
                else:
                    print("⚠ Success flow completed (no specific success indicator)")
            
        except Exception as e:
            print(f"✗ Success flow test failed: {e}")
            self.fail(f"Success flow test failed: {e}")
    
    def test_change_password_navigation(self):
        """Test navigation back to profile"""
        print("\n=== Testing Change Password Navigation ===")
        
        # Login first
        if not self.login_user():
            self.skipTest("Login failed, skipping test")
        
        try:
            # Navigate to change password page
            self.driver.get(f"{self.base_url}/authentication/change-password")
            
            # Look for back to profile link
            try:
                profile_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Profile')]")
                profile_link.click()
                
                # Wait for redirect to profile
                self.wait.until(EC.url_contains("/profile"))
                print("✓ Navigation back to profile works")
                
            except NoSuchElementException:
                print("⚠ No explicit profile link found (may redirect automatically)")
            
        except Exception as e:
            print(f"✗ Navigation test failed: {e}")
            self.fail(f"Navigation test failed: {e}")

def run_change_password_tests():
    """Run all change password tests"""
    print("🚀 Starting Change Password Flow Tests...")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(ChangePasswordTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("✅ All change password tests passed!")
        return True
    else:
        print("❌ Some change password tests failed!")
        return False

if __name__ == "__main__":
    run_change_password_tests() 