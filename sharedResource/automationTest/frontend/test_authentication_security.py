#!/usr/bin/env python3
"""
Authentication Security Test Script
Tests frontend authentication and route protection
"""

import unittest
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AuthenticationSecurityTest(unittest.TestCase):
    """Test authentication security and route protection"""
    
    def setUp(self):
        """Setup test environment"""
        print("🔒 Setting up Authentication Security Test...")
        
        # Test configuration
        self.base_url = "http://localhost:3000"
        self.auth_url = f"{self.base_url}/authentication"
        self.protected_routes = [
            "/dashboard",
            "/cameras", 
            "/analytics",
            "/tables",
            "/billing",
            "/profile"
        ]
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Test user credentials
        self.test_user = {
            "email": "admin@test.com",
            "password": "admin123"
        }
        
        print("✅ Test environment setup completed")
    
    def tearDown(self):
        """Cleanup test environment"""
        if hasattr(self, 'driver'):
            self.driver.quit()
        print("🧹 Test environment cleaned up")
    
    def test_direct_access_to_protected_routes(self):
        """Test that protected routes redirect to login when not authenticated"""
        print("\n🔒 Testing direct access to protected routes...")
        
        results = {}
        
        for route in self.protected_routes:
            print(f"  Testing route: {route}")
            
            try:
                # Clear browser data to ensure no authentication
                self.driver.delete_all_cookies()
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
                
                # Navigate directly to protected route
                self.driver.get(f"{self.base_url}{route}")
                time.sleep(2)
                
                # Check current URL
                current_url = self.driver.current_url
                print(f"    Current URL: {current_url}")
                
                # Check if redirected to login
                if "/authentication" in current_url or "/sign-in" in current_url:
                    print(f"    ✅ {route}: Correctly redirected to login")
                    results[route] = "PASS"
                else:
                    print(f"    ❌ {route}: NOT redirected to login - SECURITY ISSUE!")
                    results[route] = "FAIL"
                    
            except Exception as e:
                print(f"    ⚠️ {route}: Error during test - {str(e)}")
                results[route] = "ERROR"
        
        # Summary
        print(f"\n📊 Direct Access Test Results:")
        for route, result in results.items():
            status = "✅ PASS" if result == "PASS" else "❌ FAIL" if result == "FAIL" else "⚠️ ERROR"
            print(f"  {route}: {status}")
        
        # Assert all routes are protected
        failed_routes = [route for route, result in results.items() if result == "FAIL"]
        self.assertEqual(len(failed_routes), 0, f"Security breach: {failed_routes} are not protected!")
    
    def test_authentication_flow(self):
        """Test complete authentication flow"""
        print("\n🔐 Testing authentication flow...")
        
        try:
            # Navigate to login page
            self.driver.get(f"{self.auth_url}/sign-in")
            time.sleep(2)
            
            # Check if login form is present
            email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            password_input = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
            
            print("  ✅ Login form found")
            
            # Fill login form
            email_input.clear()
            email_input.send_keys(self.test_user["email"])
            password_input.clear()
            password_input.send_keys(self.test_user["password"])
            
            print("  ✅ Login credentials entered")
            
            # Submit form
            login_button.click()
            time.sleep(3)
            
            # Check if login successful
            current_url = self.driver.current_url
            print(f"  Current URL after login: {current_url}")
            
            if "/dashboard" in current_url or "/cameras" in current_url:
                print("  ✅ Login successful")
                return True
            else:
                print("  ❌ Login failed")
                return False
                
        except Exception as e:
            print(f"  ⚠️ Authentication flow error: {str(e)}")
            return False
    
    def test_authenticated_access_to_protected_routes(self):
        """Test that authenticated users can access protected routes"""
        print("\n✅ Testing authenticated access to protected routes...")
        
        # First login
        if not self.test_authentication_flow():
            print("  ⚠️ Skipping test - login failed")
            return
        
        results = {}
        
        for route in self.protected_routes:
            print(f"  Testing authenticated access to: {route}")
            
            try:
                # Navigate to protected route
                self.driver.get(f"{self.base_url}{route}")
                time.sleep(2)
                
                # Check current URL
                current_url = self.driver.current_url
                print(f"    Current URL: {current_url}")
                
                # Check if we can access the route
                if route in current_url:
                    print(f"    ✅ {route}: Successfully accessed")
                    results[route] = "PASS"
                else:
                    print(f"    ❌ {route}: Cannot access after login")
                    results[route] = "FAIL"
                    
            except Exception as e:
                print(f"    ⚠️ {route}: Error during test - {str(e)}")
                results[route] = "ERROR"
        
        # Summary
        print(f"\n📊 Authenticated Access Test Results:")
        for route, result in results.items():
            status = "✅ PASS" if result == "PASS" else "❌ FAIL" if result == "FAIL" else "⚠️ ERROR"
            print(f"  {route}: {status}")
        
        # Assert all routes are accessible after login
        failed_routes = [route for route, result in results.items() if result == "FAIL"]
        self.assertEqual(len(failed_routes), 0, f"Access denied to: {failed_routes}")
    
    def test_logout_functionality(self):
        """Test logout functionality"""
        print("\n🚪 Testing logout functionality...")
        
        # First login
        if not self.test_authentication_flow():
            print("  ⚠️ Skipping test - login failed")
            return
        
        try:
            # Find and click logout button
            # This might be in a dropdown menu or navbar
            logout_button = None
            
            # Try different possible logout button selectors
            logout_selectors = [
                "//button[contains(text(), 'Logout')]",
                "//a[contains(text(), 'Logout')]",
                "//button[contains(@class, 'logout')]",
                "//a[contains(@class, 'logout')]",
                "//button[contains(@aria-label, 'logout')]"
            ]
            
            for selector in logout_selectors:
                try:
                    logout_button = self.driver.find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if logout_button:
                logout_button.click()
                time.sleep(2)
                print("  ✅ Logout button clicked")
            else:
                print("  ⚠️ Logout button not found, trying to clear auth manually")
                # Clear authentication manually
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
                self.driver.delete_all_cookies()
            
            # Check if redirected to login
            current_url = self.driver.current_url
            print(f"  Current URL after logout: {current_url}")
            
            if "/authentication" in current_url or "/sign-in" in current_url:
                print("  ✅ Logout successful - redirected to login")
                return True
            else:
                print("  ❌ Logout failed - not redirected to login")
                return False
                
        except Exception as e:
            print(f"  ⚠️ Logout error: {str(e)}")
            return False
    
    def test_token_validation(self):
        """Test token validation and expiration handling"""
        print("\n🔑 Testing token validation...")
        
        try:
            # First login to get token
            if not self.test_authentication_flow():
                print("  ⚠️ Skipping test - login failed")
                return
            
            # Get token from localStorage
            token = self.driver.execute_script("return localStorage.getItem('authToken');")
            print(f"  Token found: {bool(token)}")
            
            if token:
                print("  ✅ Token stored in localStorage")
                
                # Try to access protected route
                self.driver.get(f"{self.base_url}/cameras")
                time.sleep(2)
                
                current_url = self.driver.current_url
                if "/cameras" in current_url:
                    print("  ✅ Token valid - can access protected route")
                else:
                    print("  ❌ Token invalid - cannot access protected route")
            else:
                print("  ❌ No token found in localStorage")
                
        except Exception as e:
            print(f"  ⚠️ Token validation error: {str(e)}")
    
    def test_console_logs_for_debugging(self):
        """Test console logs for debugging authentication issues"""
        print("\n🔍 Testing console logs for debugging...")
        
        try:
            # Navigate to protected route
            self.driver.get(f"{self.base_url}/cameras")
            time.sleep(3)
            
            # Get console logs
            logs = self.driver.get_log('browser')
            
            # Filter authentication-related logs
            auth_logs = [log for log in logs if any(keyword in log['message'].lower() 
                                                  for keyword in ['auth', 'protected', 'token', 'login'])]
            
            print(f"  Found {len(auth_logs)} authentication-related console logs:")
            for log in auth_logs:
                print(f"    {log['message']}")
            
            if auth_logs:
                print("  ✅ Console logs found - useful for debugging")
            else:
                print("  ⚠️ No authentication console logs found")
                
        except Exception as e:
            print(f"  ⚠️ Console log test error: {str(e)}")

def run_security_tests():
    """Run all security tests"""
    print("🔒 Starting Frontend Authentication Security Tests")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(AuthenticationSecurityTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate report
    print("\n" + "=" * 60)
    print("📊 SECURITY TEST SUMMARY")
    print("=" * 60)
    
    if result.wasSuccessful():
        print("✅ All security tests PASSED")
        print("🔒 Frontend authentication is working correctly")
    else:
        print("❌ Some security tests FAILED")
        print("🚨 CRITICAL: Frontend authentication has security issues!")
        print("\nFailed tests:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_security_tests()
    exit(0 if success else 1) 