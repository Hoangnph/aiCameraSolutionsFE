#!/usr/bin/env python3
"""
Authentication Flow Automation Tests
Tests the complete authentication flow including registration and login
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))

from test_utils import TestUtils

class AuthenticationFlowTest:
    """Test class for authentication flow automation"""
    
    def __init__(self, base_url="http://localhost:3000", headless=True):
        self.base_url = base_url
        self.headless = headless
        self.driver = None
        self.test_utils = TestUtils()
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("auth_flow_test")
        
        # Test data with proper validation rules
        self.test_user = {
            "username": f"testuser_{int(time.time())}",
            "email": f"testuser_{int(time.time())}@example.com",
            "password": "TestPass123!",
            "confirmPassword": "TestPass123!",
            "firstName": "Test",
            "lastName": "User",
            "registrationCode": "REG001"
        }
        
        # Test results
        self.test_results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Try to use the TestUtils setup method first
            try:
                self.driver = TestUtils.setup_chrome_driver(headless=self.headless)
            except Exception:
                # Fallback to direct Chrome setup
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.driver.implicitly_wait(10)
            self.logger.info("WebDriver setup completed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {e}")
            return False
    
    def teardown_driver(self):
        """Clean up WebDriver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver cleanup completed")
    
    def navigate_to_auth_page(self, auth_type="login"):
        """Navigate to authentication page"""
        try:
            if auth_type == "register":
                url = f"{self.base_url}/authentication/sign-up"
            else:
                url = f"{self.base_url}/authentication/sign-in"
            
            self.driver.get(url)
            time.sleep(2)  # Wait for page load
            self.logger.info(f"Navigated to {auth_type} page: {url}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to {auth_type} page: {e}")
            return False
    
    def test_registration_flow(self):
        """Test complete registration flow with success dialog"""
        self.test_results["total_tests"] += 1
        
        try:
            self.logger.info("Starting registration flow test")
            
            # Navigate to registration page
            if not self.navigate_to_auth_page("register"):
                raise Exception("Failed to navigate to registration page")
            
            # Fill registration form
            self.logger.info("Filling registration form")
            
            # First Name
            first_name_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="firstName"]')
            first_name_input.send_keys(self.test_user["firstName"])
            
            # Last Name
            last_name_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="lastName"]')
            last_name_input.send_keys(self.test_user["lastName"])
            
            # Username
            username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
            username_input.send_keys(self.test_user["username"])
            
            # Email
            email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
            email_input.send_keys(self.test_user["email"])
            
            # Password
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            password_input.send_keys(self.test_user["password"])
            
            # Confirm Password
            confirm_password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="confirmPassword"]')
            confirm_password_input.send_keys(self.test_user["confirmPassword"])
            
            # Registration Code
            code_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="registrationCode"]')
            code_input.send_keys(self.test_user["registrationCode"])
            
            # Accept Terms
            terms_checkbox = self.driver.find_element(By.CSS_SELECTOR, 'input[name="acceptTerms"]')
            if not terms_checkbox.is_selected():
                terms_checkbox.click()
            
            # Submit form
            self.logger.info("Submitting registration form")
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            # Wait for success dialog
            self.logger.info("Waiting for success dialog")
            wait = WebDriverWait(self.driver, 10)
            success_dialog = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Đăng ký thành công!')]"))
            )
            
            # Verify dialog content
            dialog_content = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Bạn đã đăng ký tài khoản thành công')]")
            assert dialog_content.is_displayed(), "Success dialog content not displayed"
            
            # Click "Đăng nhập ngay" button
            self.logger.info("Clicking login button in dialog")
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="success-dialog-login-button"]')
            login_button.click()
            
            # Verify redirect to login page
            wait.until(lambda driver: "/authentication/sign-in" in driver.current_url)
            self.logger.info("Successfully redirected to login page")
            
            self.test_results["passed"] += 1
            self.logger.info("Registration flow test PASSED")
            return True
            
        except Exception as e:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"Registration flow test failed: {str(e)}")
            self.logger.error(f"Registration flow test FAILED: {e}")
            return False
    
    def test_login_flow(self):
        """Test complete login flow with direct dashboard redirect"""
        self.test_results["total_tests"] += 1
        
        try:
            self.logger.info("Starting login flow test")
            
            # Navigate to login page
            if not self.navigate_to_auth_page("login"):
                raise Exception("Failed to navigate to login page")
            
            # Fill login form
            self.logger.info("Filling login form")
            
            # Username/Email
            username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
            username_input.send_keys(self.test_user["username"])
            
            # Password
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            password_input.send_keys(self.test_user["password"])
            
            # Submit form
            self.logger.info("Submitting login form")
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            # Wait for redirect to dashboard
            self.logger.info("Waiting for redirect to dashboard")
            wait = WebDriverWait(self.driver, 10)
            wait.until(lambda driver: "/dashboard" in driver.current_url)
            
            # Verify dashboard page loaded
            dashboard_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dashboard') or contains(text(), 'Dashboard')]"))
            )
            
            self.test_results["passed"] += 1
            self.logger.info("Login flow test PASSED")
            return True
            
        except Exception as e:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"Login flow test failed: {str(e)}")
            self.logger.error(f"Login flow test FAILED: {e}")
            return False
    
    def test_registration_validation(self):
        """Test registration form validation with correct data"""
        self.test_results["total_tests"] += 1
        
        try:
            self.logger.info("Starting registration validation test")
            
            # Navigate to registration page
            if not self.navigate_to_auth_page("register"):
                raise Exception("Failed to navigate to registration page")
            
            # Fill form with valid data according to validation rules
            form_data = {
                'username': 'testuser123',
                'email': 'test@example.com',
                'password': 'TestPass123!',
                'confirmPassword': 'TestPass123!',
                'firstName': 'Test',
                'lastName': 'User',
                'registrationCode': 'REG001'
            }
            
            # Fill each field
            for field_name, value in form_data.items():
                try:
                    field = self.driver.find_element(By.CSS_SELECTOR, f'input[name="{field_name}"]')
                    field.clear()
                    field.send_keys(value)
                    time.sleep(0.5)
                except NoSuchElementException:
                    self.logger.warning(f"Field {field_name} not found")
            
            # Try to submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            # Wait for response
            time.sleep(3)
            
            self.test_results["passed"] += 1
            self.logger.info("Registration validation test PASSED")
            return True
            
        except Exception as e:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"Registration validation test failed: {str(e)}")
            self.logger.error(f"Registration validation test FAILED: {e}")
            return False
    
    def test_login_validation(self):
        """Test login form validation"""
        self.test_results["total_tests"] += 1
        
        try:
            self.logger.info("Starting login validation test")
            
            # Navigate to login page
            if not self.navigate_to_auth_page("login"):
                raise Exception("Failed to navigate to login page")
            
            # Try to submit empty form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            # Check for validation errors
            wait = WebDriverWait(self.driver, 5)
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, '.MuiFormHelperText-root.Mui-error')
            
            assert len(error_elements) > 0, "No validation errors displayed for empty form"
            
            self.test_results["passed"] += 1
            self.logger.info("Login validation test PASSED")
            return True
            
        except Exception as e:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"Login validation test failed: {str(e)}")
            self.logger.error(f"Login validation test FAILED: {e}")
            return False
    
    def test_password_visibility_toggle(self):
        """Test password visibility toggle functionality"""
        self.test_results["total_tests"] += 1
        
        try:
            self.logger.info("Starting password visibility toggle test")
            
            # Navigate to login page
            if not self.navigate_to_auth_page("login"):
                raise Exception("Failed to navigate to login page")
            
            # Find password input and toggle button
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            toggle_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="password-toggle"]')
            
            # Check initial state (password should be hidden)
            assert password_input.get_attribute("type") == "password", "Password should be hidden initially"
            
            # Click toggle button
            toggle_button.click()
            
            # Check if password is now visible
            assert password_input.get_attribute("type") == "text", "Password should be visible after toggle"
            
            # Click toggle button again
            toggle_button.click()
            
            # Check if password is hidden again
            assert password_input.get_attribute("type") == "password", "Password should be hidden after second toggle"
            
            self.test_results["passed"] += 1
            self.logger.info("Password visibility toggle test PASSED")
            return True
            
        except Exception as e:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"Password visibility toggle test failed: {str(e)}")
            self.logger.error(f"Password visibility toggle test FAILED: {e}")
            return False
    
    def test_error_handling(self):
        """Test error handling for invalid credentials"""
        self.test_results["total_tests"] += 1
        
        try:
            self.logger.info("Starting error handling test")
            
            # Navigate to login page
            if not self.navigate_to_auth_page("login"):
                raise Exception("Failed to navigate to login page")
            
            # Fill form with invalid credentials
            username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
            username_input.send_keys("invalid_user")
            
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            password_input.send_keys("invalid_password")
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            # Wait for error message
            wait = WebDriverWait(self.driver, 10)
            error_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="login-error"]'))
            )
            
            assert error_element.is_displayed(), "Error message should be displayed"
            
            self.test_results["passed"] += 1
            self.logger.info("Error handling test PASSED")
            return True
            
        except Exception as e:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"Error handling test failed: {str(e)}")
            self.logger.error(f"Error handling test FAILED: {e}")
            return False
    
    def run_all_tests(self):
        """Run all authentication flow tests"""
        self.logger.info("Starting Authentication Flow Tests")
        
        if not self.setup_driver():
            self.logger.error("Failed to setup WebDriver")
            return False
        
        try:
            # Run all tests
            tests = [
                self.test_registration_validation,
                self.test_login_validation,
                self.test_password_visibility_toggle,
                self.test_error_handling,
                self.test_registration_flow,
                self.test_login_flow
            ]
            
            for test in tests:
                try:
                    test()
                    time.sleep(2)  # Brief pause between tests
                except Exception as e:
                    self.logger.error(f"Test {test.__name__} failed with exception: {e}")
            
            # Print results
            self.print_results()
            
            return self.test_results["failed"] == 0
            
        finally:
            self.teardown_driver()
    
    def print_results(self):
        """Print test results"""
        print("\n" + "="*50)
        print("AUTHENTICATION FLOW TEST RESULTS")
        print("="*50)
        print(f"Total Tests: {self.test_results['total_tests']}")
        print(f"Passed: {self.test_results['passed']}")
        print(f"Failed: {self.test_results['failed']}")
        print(f"Success Rate: {(self.test_results['passed']/self.test_results['total_tests']*100):.1f}%")
        
        if self.test_results["errors"]:
            print("\nErrors:")
            for error in self.test_results["errors"]:
                print(f"  - {error}")
        
        print("="*50)
        
        # Save results to file
        results_file = os.path.join(
            os.path.dirname(__file__), 
            "..", "results", 
            f"auth_flow_results_{int(time.time())}.json"
        )
        
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        self.logger.info(f"Results saved to {results_file}")

def main():
    """Main function to run authentication flow tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Authentication Flow Automation Tests")
    parser.add_argument("--base-url", default="http://localhost:3000", help="Base URL for testing")
    parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
    parser.add_argument("--no-headless", action="store_true", help="Run tests with browser visible")
    
    args = parser.parse_args()
    
    headless = args.headless or not args.no_headless
    
    test_runner = AuthenticationFlowTest(
        base_url=args.base_url,
        headless=headless
    )
    
    success = test_runner.run_all_tests()
    
    if success:
        print("\n✅ All authentication flow tests PASSED!")
        sys.exit(0)
    else:
        print("\n❌ Some authentication flow tests FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main() 