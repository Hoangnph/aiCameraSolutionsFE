#!/usr/bin/env python3
"""
Simple Authentication Loading Test Script
Tests the authentication loading logic using HTTP requests
"""

import time
import requests
import json
import os

class SimpleAuthTest:
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.results = {
            "test_name": "Simple Authentication Loading Test",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tests": []
        }
    
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
    
    def test_signin_page_loads(self):
        """Test sign-in page loads without infinite loading"""
        try:
            response = requests.get(f"{self.base_url}/authentication/sign-in", timeout=10)
            
            if response.status_code == 200:
                # Check if page contains sign-in form elements
                content = response.text.lower()
                if "sign in" in content or "login" in content or "email" in content:
                    self.log_test("Sign-in Page Loading", "PASS", "Page loaded successfully")
                    return True
                else:
                    self.log_test("Sign-in Page Loading", "FAIL", "Page content doesn't match expected")
                    return False
            else:
                self.log_test("Sign-in Page Loading", "FAIL", f"Page returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Sign-in Page Loading", "FAIL", f"Error loading page: {str(e)}")
            return False
    
    def test_dashboard_redirects_when_not_authenticated(self):
        """Test dashboard redirects to sign-in when not authenticated"""
        try:
            response = requests.get(f"{self.base_url}/dashboard", timeout=10, allow_redirects=False)
            
            if response.status_code in [301, 302, 303, 307, 308]:
                # Check if redirect is to sign-in
                location = response.headers.get('location', '')
                if '/authentication/sign-in' in location:
                    self.log_test("Dashboard Redirect", "PASS", "Redirected to sign-in page")
                    return True
                else:
                    self.log_test("Dashboard Redirect", "FAIL", f"Redirected to wrong location: {location}")
                    return False
            else:
                self.log_test("Dashboard Redirect", "FAIL", f"No redirect, status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard Redirect", "FAIL", f"Error testing redirect: {str(e)}")
            return False
    
    def test_no_menu_on_auth_pages(self):
        """Test that menu/sidenav is not present on authentication pages"""
        try:
            response = requests.get(f"{self.base_url}/authentication/sign-in", timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for menu/sidenav indicators
                menu_indicators = ['sidenav', 'navigation', 'menu', 'sidebar']
                has_menu = any(indicator in content for indicator in menu_indicators)
                
                if not has_menu:
                    self.log_test("No Menu on Auth Pages", "PASS", "Menu not present on sign-in page")
                    return True
                else:
                    self.log_test("No Menu on Auth Pages", "FAIL", "Menu elements found in page content")
                    return False
            else:
                self.log_test("No Menu on Auth Pages", "FAIL", f"Page returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("No Menu on Auth Pages", "FAIL", f"Error checking menu: {str(e)}")
            return False
    
    def test_page_load_time(self):
        """Test that pages load quickly without hanging"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/authentication/sign-in", timeout=10)
            load_time = time.time() - start_time
            
            if response.status_code == 200 and load_time < 5:  # Should load within 5 seconds
                self.log_test("Page Load Time", "PASS", f"Page loaded in {load_time:.2f} seconds")
                return True
            elif load_time >= 5:
                self.log_test("Page Load Time", "FAIL", f"Page took too long to load: {load_time:.2f} seconds")
                return False
            else:
                self.log_test("Page Load Time", "FAIL", f"Page returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Page Load Time", "FAIL", f"Error testing load time: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Simple Authentication Loading Tests...")
        print("=" * 60)
        
        # Run tests
        tests = [
            self.test_server_status,
            self.test_signin_page_loads,
            self.test_dashboard_redirects_when_not_authenticated,
            self.test_no_menu_on_auth_pages,
            self.test_page_load_time
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
        filename = f"simple_auth_test_results_{timestamp}.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📄 Results saved to: {filepath}")

def main():
    """Main test function"""
    test = SimpleAuthTest()
    
    try:
        success = test.run_all_tests()
        test.save_results()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Test suite crashed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 