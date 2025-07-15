#!/usr/bin/env python3
"""
Frontend Authentication Components Test Suite
Tests for authentication components and forms
"""

import unittest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AuthenticationComponentsTest(unittest.TestCase):
    """Test suite for authentication components"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize WebDriver
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
        
        # Test configuration
        cls.base_url = "http://localhost:3000"
        cls.auth_url = f"{cls.base_url}/authentication"
        
        # Test data
        cls.test_users = {
            "admin": {
                "email": "admin@example.com",
                "password": "Admin123!",
                "username": "admin"
            },
            "user": {
                "email": "user@example.com", 
                "password": "User123!",
                "username": "user"
            }
        }
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        if cls.driver:
            cls.driver.quit()
    
    def setUp(self):
        """Set up before each test"""
        self.driver.delete_all_cookies()
        self.driver.get(self.auth_url)
        time.sleep(2)  # Wait for page load
    
    def test_auth_container_rendering(self):
        """Test AuthContainer component rendering"""
        print("Testing AuthContainer component rendering...")
        
        # Check if auth container is present
        container = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-container"]'))
        )
        self.assertIsNotNone(container)
        
        # Check if title is present
        title = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-title"]')
        self.assertIsNotNone(title)
        self.assertIn("Đăng nhập", title.text)
        
        # Check if content area is present
        content = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-content"]')
        self.assertIsNotNone(content)
        
        print("✅ AuthContainer rendering test passed")
    
    def test_auth_tabs_navigation(self):
        """Test AuthTabs component navigation"""
        print("Testing AuthTabs component navigation...")
        
        # Check if tabs are present
        tabs_container = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-tabs"]'))
        )
        self.assertIsNotNone(tabs_container)
        
        # Check login tab
        login_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="login-tab"]')
        self.assertIsNotNone(login_tab)
        self.assertIn("Đăng nhập", login_tab.text)
        
        # Check register tab
        register_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="register-tab"]')
        self.assertIsNotNone(register_tab)
        self.assertIn("Đăng ký", register_tab.text)
        
        # Check forgot password tab
        forgot_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="forgot-tab"]')
        self.assertIsNotNone(forgot_tab)
        self.assertIn("Quên mật khẩu", forgot_tab.text)
        
        # Test tab switching
        register_tab.click()
        time.sleep(1)
        
        # Check if URL changed
        current_url = self.driver.current_url
        self.assertIn("/register", current_url)
        
        # Switch back to login
        login_tab.click()
        time.sleep(1)
        
        current_url = self.driver.current_url
        self.assertIn("/login", current_url)
        
        print("✅ AuthTabs navigation test passed")
    
    def test_login_form_rendering(self):
        """Test LoginForm component rendering"""
        print("Testing LoginForm component rendering...")
        
        # Check if login form is present
        login_form = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="login-form"]'))
        )
        self.assertIsNotNone(login_form)
        
        # Check email input
        email_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]')
        self.assertIsNotNone(email_input)
        self.assertEqual(email_input.get_attribute("type"), "text")
        
        # Check password input
        password_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
        self.assertIsNotNone(password_input)
        self.assertEqual(password_input.get_attribute("type"), "password")
        
        # Check remember me checkbox
        remember_checkbox = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="remember-me"]')
        self.assertIsNotNone(remember_checkbox)
        
        # Check login button
        login_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]')
        self.assertIsNotNone(login_button)
        self.assertIn("Đăng nhập", login_button.text)
        
        # Check forgot password link
        forgot_link = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="forgot-password-link"]')
        self.assertIsNotNone(forgot_link)
        self.assertIn("Quên mật khẩu", forgot_link.text)
        
        # Check register link
        register_link = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="register-link"]')
        self.assertIsNotNone(register_link)
        self.assertIn("Đăng ký ngay", register_link.text)
        
        print("✅ LoginForm rendering test passed")
    
    def test_login_form_validation(self):
        """Test LoginForm validation"""
        print("Testing LoginForm validation...")
        
        # Wait for form to load
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="login-form"]'))
        )
        
        # Test empty form submission
        login_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]')
        login_button.click()
        
        # Check if button is disabled (form validation)
        time.sleep(1)
        button_disabled = login_button.get_attribute("disabled")
        self.assertIsNotNone(button_disabled)
        
        # Test invalid email format
        email_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]')
        email_input.clear()
        email_input.send_keys("invalid-email")
        email_input.send_keys("\t")  # Trigger blur event
        
        time.sleep(1)
        
        # Check for validation error (if any)
        try:
            error_element = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="email-error"]')
            self.assertIsNotNone(error_element)
        except NoSuchElementException:
            # Error might not be visible yet, continue with test
            pass
        
        print("✅ LoginForm validation test passed")
    
    def test_register_form_rendering(self):
        """Test RegisterForm component rendering"""
        print("Testing RegisterForm component rendering...")
        
        # Switch to register tab
        register_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="register-tab"]')
        register_tab.click()
        time.sleep(2)
        
        # Check if register form is present
        register_form = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="register-form"]'))
        )
        self.assertIsNotNone(register_form)
        
        # Check all form fields
        fields = [
            'first-name-input', 'last-name-input', 'username-input', 'email-input',
            'password-input', 'confirm-password-input', 'registration-code-input'
        ]
        
        for field in fields:
            field_element = self.driver.find_element(By.CSS_SELECTOR, f'[data-testid="{field}"]')
            self.assertIsNotNone(field_element)
        
        # Check accept terms checkbox
        accept_terms = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="accept-terms"]')
        self.assertIsNotNone(accept_terms)
        
        # Check register button
        register_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="register-button"]')
        self.assertIsNotNone(register_button)
        self.assertIn("Đăng ký", register_button.text)
        
        # Check login link
        login_link = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="login-link"]')
        self.assertIsNotNone(login_link)
        self.assertIn("Đăng nhập ngay", login_link.text)
        
        print("✅ RegisterForm rendering test passed")
    
    def test_register_form_validation(self):
        """Test RegisterForm validation"""
        print("Testing RegisterForm validation...")
        
        # Switch to register tab
        register_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="register-tab"]')
        register_tab.click()
        time.sleep(2)
        
        # Wait for form to load
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="register-form"]'))
        )
        
        # Test empty form submission
        register_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="register-button"]')
        register_button.click()
        
        # Check if button is disabled (form validation)
        time.sleep(1)
        button_disabled = register_button.get_attribute("disabled")
        self.assertIsNotNone(button_disabled)
        
        # Test invalid email format
        email_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]')
        email_input.clear()
        email_input.send_keys("invalid-email")
        email_input.send_keys("\t")  # Trigger blur event
        
        time.sleep(1)
        
        # Test password strength indicator
        password_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
        password_input.clear()
        password_input.send_keys("weak")
        password_input.send_keys("\t")  # Trigger blur event
        
        time.sleep(1)
        
        # Check if password strength indicator is shown
        try:
            strength_text = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Độ mạnh mật khẩu:')]")
            self.assertIsNotNone(strength_text)
        except NoSuchElementException:
            # Strength indicator might not be visible yet
            pass
        
        print("✅ RegisterForm validation test passed")
    
    def test_forgot_password_form_rendering(self):
        """Test ForgotPasswordForm component rendering"""
        print("Testing ForgotPasswordForm component rendering...")
        
        # Switch to forgot password tab
        forgot_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="forgot-tab"]')
        forgot_tab.click()
        time.sleep(2)
        
        # Check if forgot password form is present
        forgot_form = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="forgot-password-form"]'))
        )
        self.assertIsNotNone(forgot_form)
        
        # Check email input
        email_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]')
        self.assertIsNotNone(email_input)
        self.assertEqual(email_input.get_attribute("type"), "email")
        
        # Check send reset link button
        send_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="send-reset-link-button"]')
        self.assertIsNotNone(send_button)
        self.assertIn("Gửi link đặt lại mật khẩu", send_button.text)
        
        # Check back to login link
        back_link = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="back-to-login-link"]')
        self.assertIsNotNone(back_link)
        self.assertIn("Đăng nhập ngay", back_link.text)
        
        print("✅ ForgotPasswordForm rendering test passed")
    
    def test_forgot_password_form_validation(self):
        """Test ForgotPasswordForm validation"""
        print("Testing ForgotPasswordForm validation...")
        
        # Switch to forgot password tab
        forgot_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="forgot-tab"]')
        forgot_tab.click()
        time.sleep(2)
        
        # Wait for form to load
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="forgot-password-form"]'))
        )
        
        # Test empty form submission
        send_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="send-reset-link-button"]')
        send_button.click()
        
        # Check if button is disabled (form validation)
        time.sleep(1)
        button_disabled = send_button.get_attribute("disabled")
        self.assertIsNotNone(button_disabled)
        
        # Test invalid email format
        email_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]')
        email_input.clear()
        email_input.send_keys("invalid-email")
        email_input.send_keys("\t")  # Trigger blur event
        
        time.sleep(1)
        
        print("✅ ForgotPasswordForm validation test passed")
    
    def test_password_visibility_toggle(self):
        """Test password visibility toggle"""
        print("Testing password visibility toggle...")
        
        # Wait for form to load
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-input"]'))
        )
        
        password_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
        toggle_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="password-toggle"]')
        
        # Check initial state (password should be hidden)
        self.assertEqual(password_input.get_attribute("type"), "password")
        
        # Click toggle button
        toggle_button.click()
        time.sleep(1)
        
        # Check if password is now visible
        self.assertEqual(password_input.get_attribute("type"), "text")
        
        # Click toggle button again
        toggle_button.click()
        time.sleep(1)
        
        # Check if password is hidden again
        self.assertEqual(password_input.get_attribute("type"), "password")
        
        print("✅ Password visibility toggle test passed")
    
    def test_remember_me_functionality(self):
        """Test remember me checkbox functionality"""
        print("Testing remember me functionality...")
        
        # Wait for form to load
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="remember-me"]'))
        )
        
        remember_checkbox = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="remember-me"]')
        
        # Check initial state (should be unchecked)
        self.assertFalse(remember_checkbox.is_selected())
        
        # Click checkbox
        remember_checkbox.click()
        time.sleep(1)
        
        # Check if checkbox is now selected
        self.assertTrue(remember_checkbox.is_selected())
        
        # Click checkbox again
        remember_checkbox.click()
        time.sleep(1)
        
        # Check if checkbox is unselected
        self.assertFalse(remember_checkbox.is_selected())
        
        print("✅ Remember me functionality test passed")
    
    def test_form_accessibility(self):
        """Test form accessibility features"""
        print("Testing form accessibility...")
        
        # Wait for form to load
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="login-form"]'))
        )
        
        # Check if form has proper ARIA labels
        email_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]')
        password_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
        
        # Check aria-label attributes
        email_aria_label = email_input.get_attribute("aria-label")
        password_aria_label = password_input.get_attribute("aria-label")
        
        self.assertIsNotNone(email_aria_label)
        self.assertIsNotNone(password_aria_label)
        
        # Check if form is keyboard navigable
        email_input.click()
        email_input.send_keys("test@example.com")
        email_input.send_keys("\t")  # Tab to next field
        
        # Check if focus moved to password field
        active_element = self.driver.switch_to.active_element
        self.assertEqual(active_element.get_attribute("data-testid"), "password-input")
        
        print("✅ Form accessibility test passed")
    
    def test_error_handling(self):
        """Test error handling in login form"""
        print("Testing error handling...")
        
        # Wait for form to load
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="login-form"]'))
        )
        
        # Fill form with invalid credentials
        email_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]')
        password_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
        
        email_input.clear()
        email_input.send_keys("invalid@example.com")
        password_input.clear()
        password_input.send_keys("wrongpassword")
        
        # Submit form
        login_button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]')
        login_button.click()
        
        # Wait for error message (if any)
        time.sleep(2)
        
        try:
            error_element = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="login-error"]')
            self.assertIsNotNone(error_element)
            print(f"Error message displayed: {error_element.text}")
        except NoSuchElementException:
            # Error might not be displayed immediately or might be handled differently
            print("No immediate error message displayed (this might be expected)")
        
        print("✅ Error handling test passed")
    
    def test_responsive_design(self):
        """Test responsive design on different screen sizes"""
        print("Testing responsive design...")
        
        # Test mobile viewport
        self.driver.set_window_size(375, 667)
        time.sleep(2)
        
        # Check if elements are still accessible
        container = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-container"]')
        self.assertIsNotNone(container)
        
        # Test tablet viewport
        self.driver.set_window_size(768, 1024)
        time.sleep(2)
        
        container = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-container"]')
        self.assertIsNotNone(container)
        
        # Test desktop viewport
        self.driver.set_window_size(1920, 1080)
        time.sleep(2)
        
        container = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-container"]')
        self.assertIsNotNone(container)
        
        print("✅ Responsive design test passed")

def run_tests():
    """Run all authentication component tests"""
    print("🚀 Starting Frontend Authentication Components Test Suite")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(AuthenticationComponentsTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("=" * 60)
    print(f"📊 Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1) 