#!/usr/bin/env python3
"""
Authentication Loading Test Script
Tests the authentication loading logic to ensure no infinite loading
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import os

class AuthLoadingTest:
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.results = {
            "test_name": "Authentication Loading Test",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tests": []
        }
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def log_test(self, test_name, status, message=""):
        """Log test result"""
        test_result = {
            "name": test_name,
            "status": status,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results["tests"].append(test_result)
        print(f"✅ {test_name}: {status} - {message}")
    
    def test_server_status(self):
        """Test if server is running"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                self.log_test("Server Status", "PASS", "Server is running")
                return True
            else:
                self.log_test("Server Status", "FAIL", f"Server returned {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Status", "FAIL", f"Server not accessible: {str(e)}")
            return False
    
    def test_signin_page_loading(self):
        """Test sign-in page loads without infinite loading"""
        try:
            self.driver.get(f"{self.base_url}/authentication/sign-in")
            time.sleep(3)  # Wait for page to load
            
            # Check if page loaded successfully
            page_title = self.driver.title
            if "Sign In" in page_title or "Login" in page_title:
                self.log_test("Sign-in Page Loading", "PASS", "Page loaded successfully")
                return True
            else:
                self.log_test("Sign-in Page Loading", "FAIL", f"Unexpected title: {page_title}")
                return False
                
        except Exception as e:
            self.log_test("Sign-in Page Loading", "FAIL", f"Error loading page: {str(e)}")
            return False
    
    def test_dashboard_redirect_when_not_authenticated(self):
        """Test dashboard redirects to sign-in when not authenticated"""
        try:
            self.driver.get(f"{self.base_url}/dashboard")
            time.sleep(5)  # Wait for redirect
            
            current_url = self.driver.current_url
            if "/authentication/sign-in" in current_url:
                self.log_test("Dashboard Redirect", "PASS", "Redirected to sign-in page")
                return True
            else:
                self.log_test("Dashboard Redirect", "FAIL", f"Not redirected, current URL: {current_url}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard Redirect", "FAIL", f"Error testing redirect: {str(e)}")
            return False
    
    def test_no_menu_on_auth_pages(self):
        """Test that menu/sidenav is not present on authentication pages"""
        try:
            self.driver.get(f"{self.base_url}/authentication/sign-in")
            time.sleep(3)
            
            # Look for sidenav elements
            sidenav_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='sidenav'], .sidenav, nav")
            
            if len(sidenav_elements) == 0:
                self.log_test("No Menu on Auth Pages", "PASS", "Menu not present on sign-in page")
                return True
            else:
                self.log_test("No Menu on Auth Pages", "FAIL", f"Found {len(sidenav_elements)} menu elements")
                return False
                
        except Exception as e:
            self.log_test("No Menu on Auth Pages", "FAIL", f"Error checking menu: {str(e)}")
            return False
    
    def test_console_errors(self):
        """Test for console errors during page load"""
        try:
            self.driver.get(f"{self.base_url}/authentication/sign-in")
            time.sleep(3)
            
            # Get console logs
            logs = self.driver.get_log('browser')
            errors = [log for log in logs if log['level'] == 'SEVERE']
            
            if len(errors) == 0:
                self.log_test("Console Errors", "PASS", "No console errors found")
                return True
            else:
                error_messages = [error['message'] for error in errors[:3]]  # Show first 3 errors
                self.log_test("Console Errors", "FAIL", f"Found {len(errors)} errors: {error_messages}")
                return False
                
        except Exception as e:
            self.log_test("Console Errors", "FAIL", f"Error checking console: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Authentication Loading Tests...")
        print("=" * 60)
        
        # Run tests
        tests = [
            self.test_server_status,
            self.test_signin_page_loading,
            self.test_dashboard_redirect_when_not_authenticated,
            self.test_no_menu_on_auth_pages,
            self.test_console_errors
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                self.log_test(test.__name__, "ERROR", f"Test crashed: {str(e)}")
        
        # Summary
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Authentication loading logic is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the results above.")
        
        return passed == total
    
    def save_results(self):
        """Save test results to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"auth_loading_test_results_{timestamp}.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📄 Results saved to: {filepath}")
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()

def main():
    """Main test function"""
    test = AuthLoadingTest()
    
    try:
        success = test.run_all_tests()
        test.save_results()
        return 0 if success else 1
    finally:
        test.cleanup()

if __name__ == "__main__":
    exit(main()) 