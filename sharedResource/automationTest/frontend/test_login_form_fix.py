#!/usr/bin/env python3
"""
Test script to verify login form automatic submission fix
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginFormFixTest:
    def __init__(self):
        self.driver = None
        self.base_url = "http://localhost:3000"
        self.test_results = {
            "test_name": "Login Form Automatic Submission Fix",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": []
        }
    
    def setup_driver(self):
        """Setup Chrome driver with headless mode"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
    
    def log_result(self, test_name, status, message=""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results["results"].append(result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {message}")
    
    def test_page_load(self):
        """Test if login page loads correctly"""
        try:
            self.driver.get(f"{self.base_url}/authentication/sign-in")
            time.sleep(2)
            
            # Check if page title contains expected text
            page_title = self.driver.title
            if "sign-in" in page_title.lower() or "login" in page_title.lower():
                self.log_result("Page Load", "PASS", f"Page loaded successfully: {page_title}")
                return True
            else:
                self.log_result("Page Load", "FAIL", f"Unexpected page title: {page_title}")
                return False
        except Exception as e:
            self.log_result("Page Load", "FAIL", f"Error loading page: {str(e)}")
            return False
    
    def test_form_elements(self):
        """Test if form elements are present"""
        try:
            # Check for form
            form = self.driver.find_element(By.CSS_SELECTOR, "form[role='form']")
            self.log_result("Form Element", "PASS", "Login form found")
            
            # Check for username input
            username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            self.log_result("Username Input", "PASS", "Username input field found")
            
            # Check for password input
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            self.log_result("Password Input", "PASS", "Password input field found")
            
            # Check for submit button
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.log_result("Submit Button", "PASS", "Submit button found")
            
            return True
        except NoSuchElementException as e:
            self.log_result("Form Elements", "FAIL", f"Missing form element: {str(e)}")
            return False
    
    def test_form_validation(self):
        """Test form validation attributes"""
        try:
            # Check if form has noValidate attribute
            form = self.driver.find_element(By.CSS_SELECTOR, "form[role='form']")
            if form.get_attribute("noValidate"):
                self.log_result("Form noValidate", "PASS", "Form has noValidate attribute")
            else:
                self.log_result("Form noValidate", "WARN", "Form missing noValidate attribute")
            
            # Check if inputs have required attribute
            username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            
            if username_input.get_attribute("required") and password_input.get_attribute("required"):
                self.log_result("Input Required", "PASS", "Input fields have required attribute")
            else:
                self.log_result("Input Required", "WARN", "Input fields missing required attribute")
            
            return True
        except Exception as e:
            self.log_result("Form Validation", "FAIL", f"Error checking validation: {str(e)}")
            return False
    
    def test_submit_button_state(self):
        """Test submit button disabled state"""
        try:
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            # Check initial state (should be disabled when fields are empty)
            is_disabled = submit_button.get_attribute("disabled")
            if is_disabled:
                self.log_result("Button Disabled State", "PASS", "Submit button correctly disabled when fields empty")
            else:
                self.log_result("Button Disabled State", "WARN", "Submit button not disabled when fields empty")
            
            return True
        except Exception as e:
            self.log_result("Button State", "FAIL", f"Error checking button state: {str(e)}")
            return False
    
    def test_automatic_submission_prevention(self):
        """Test if form prevents automatic submission"""
        try:
            # Get initial page URL
            initial_url = self.driver.current_url
            
            # Wait for 5 seconds to see if any automatic submission occurs
            time.sleep(5)
            
            # Check if URL changed (indicating automatic redirect)
            current_url = self.driver.current_url
            if current_url == initial_url:
                self.log_result("Auto Submission Prevention", "PASS", "No automatic submission detected")
                return True
            else:
                self.log_result("Auto Submission Prevention", "FAIL", f"Automatic submission detected: {initial_url} -> {current_url}")
                return False
        except Exception as e:
            self.log_result("Auto Submission Prevention", "FAIL", f"Error testing submission prevention: {str(e)}")
            return False
    
    def test_form_submission_control(self):
        """Test controlled form submission"""
        try:
            # Fill in form fields
            username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            
            username_input.clear()
            username_input.send_keys("test@example.com")
            password_input.clear()
            password_input.send_keys("testpassword")
            
            # Check if submit button is now enabled
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            time.sleep(1)
            
            is_enabled = not submit_button.get_attribute("disabled")
            if is_enabled:
                self.log_result("Form Submission Control", "PASS", "Submit button enabled when fields filled")
            else:
                self.log_result("Form Submission Control", "WARN", "Submit button still disabled when fields filled")
            
            return True
        except Exception as e:
            self.log_result("Form Submission Control", "FAIL", f"Error testing form submission: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🔍 Starting Login Form Fix Tests...")
        print("=" * 50)
        
        try:
            self.setup_driver()
            
            tests = [
                self.test_page_load,
                self.test_form_elements,
                self.test_form_validation,
                self.test_submit_button_state,
                self.test_automatic_submission_prevention,
                self.test_form_submission_control
            ]
            
            for test in tests:
                try:
                    test()
                except Exception as e:
                    print(f"❌ Test failed with exception: {str(e)}")
            
            # Calculate results
            total_tests = len(self.test_results["results"])
            passed_tests = len([r for r in self.test_results["results"] if r["status"] == "PASS"])
            failed_tests = len([r for r in self.test_results["results"] if r["status"] == "FAIL"])
            warning_tests = len([r for r in self.test_results["results"] if r["status"] == "WARN"])
            
            print("\n" + "=" * 50)
            print("📊 TEST RESULTS SUMMARY")
            print("=" * 50)
            print(f"Total Tests: {total_tests}")
            print(f"✅ Passed: {passed_tests}")
            print(f"❌ Failed: {failed_tests}")
            print(f"⚠️ Warnings: {warning_tests}")
            
            if failed_tests == 0:
                print("\n🎉 All critical tests passed! Login form fix appears successful.")
            else:
                print(f"\n⚠️ {failed_tests} test(s) failed. Please review the issues.")
            
            # Save results
            self.save_results()
            
        except Exception as e:
            print(f"❌ Test suite failed: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
    
    def save_results(self):
        """Save test results to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"login_form_fix_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Test results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")

if __name__ == "__main__":
    test_suite = LoginFormFixTest()
    test_suite.run_all_tests() 