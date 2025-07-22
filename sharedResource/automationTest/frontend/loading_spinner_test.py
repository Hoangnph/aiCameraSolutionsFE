#!/usr/bin/env python3
"""
LoadingSpinner Test Script
Tests that LoadingSpinner component is properly imported and working
"""

import time
import requests
import json
import os

class LoadingSpinnerTest:
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.results = {
            "test_name": "LoadingSpinner Component Test",
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
    
    def test_signin_page_no_errors(self):
        """Test sign-in page loads without LoadingSpinner errors"""
        try:
            response = requests.get(f"{self.base_url}/authentication/sign-in", timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for LoadingSpinner error indicators
                error_indicators = [
                    'loadingspinner is not defined',
                    'referenceerror',
                    'loading spinner',
                    'component not found'
                ]
                
                has_errors = any(indicator in content for indicator in error_indicators)
                
                if not has_errors:
                    self.log_test("Sign-in Page No Errors", "PASS", "No LoadingSpinner errors found")
                    return True
                else:
                    self.log_test("Sign-in Page No Errors", "FAIL", "LoadingSpinner errors found in page")
                    return False
            else:
                self.log_test("Sign-in Page No Errors", "FAIL", f"Page returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Sign-in Page No Errors", "FAIL", f"Error loading page: {str(e)}")
            return False
    
    def test_signup_page_no_errors(self):
        """Test sign-up page loads without LoadingSpinner errors"""
        try:
            response = requests.get(f"{self.base_url}/authentication/sign-up", timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for LoadingSpinner error indicators
                error_indicators = [
                    'loadingspinner is not defined',
                    'referenceerror',
                    'loading spinner',
                    'component not found'
                ]
                
                has_errors = any(indicator in content for indicator in error_indicators)
                
                if not has_errors:
                    self.log_test("Sign-up Page No Errors", "PASS", "No LoadingSpinner errors found")
                    return True
                else:
                    self.log_test("Sign-up Page No Errors", "FAIL", "LoadingSpinner errors found in page")
                    return False
            else:
                self.log_test("Sign-up Page No Errors", "FAIL", f"Page returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Sign-up Page No Errors", "FAIL", f"Error loading page: {str(e)}")
            return False
    
    def test_forgot_password_no_errors(self):
        """Test forgot-password page loads without LoadingSpinner errors"""
        try:
            response = requests.get(f"{self.base_url}/authentication/forgot-password", timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for LoadingSpinner error indicators
                error_indicators = [
                    'loadingspinner is not defined',
                    'referenceerror',
                    'loading spinner',
                    'component not found'
                ]
                
                has_errors = any(indicator in content for indicator in error_indicators)
                
                if not has_errors:
                    self.log_test("Forgot Password No Errors", "PASS", "No LoadingSpinner errors found")
                    return True
                else:
                    self.log_test("Forgot Password No Errors", "FAIL", "LoadingSpinner errors found in page")
                    return False
            else:
                self.log_test("Forgot Password No Errors", "FAIL", f"Page returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Forgot Password No Errors", "FAIL", f"Error loading page: {str(e)}")
            return False
    
    def test_reset_password_no_errors(self):
        """Test reset-password page loads without LoadingSpinner errors"""
        try:
            response = requests.get(f"{self.base_url}/authentication/reset-password", timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for LoadingSpinner error indicators
                error_indicators = [
                    'loadingspinner is not defined',
                    'referenceerror',
                    'loading spinner',
                    'component not found'
                ]
                
                has_errors = any(indicator in content for indicator in error_indicators)
                
                if not has_errors:
                    self.log_test("Reset Password No Errors", "PASS", "No LoadingSpinner errors found")
                    return True
                else:
                    self.log_test("Reset Password No Errors", "FAIL", "LoadingSpinner errors found in page")
                    return False
            else:
                self.log_test("Reset Password No Errors", "FAIL", f"Page returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Reset Password No Errors", "FAIL", f"Error loading page: {str(e)}")
            return False
    
    def test_dashboard_no_errors(self):
        """Test dashboard page loads without LoadingSpinner errors"""
        try:
            response = requests.get(f"{self.base_url}/dashboard", timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for LoadingSpinner error indicators
                error_indicators = [
                    'loadingspinner is not defined',
                    'referenceerror',
                    'loading spinner',
                    'component not found'
                ]
                
                has_errors = any(indicator in content for indicator in error_indicators)
                
                if not has_errors:
                    self.log_test("Dashboard No Errors", "PASS", "No LoadingSpinner errors found")
                    return True
                else:
                    self.log_test("Dashboard No Errors", "FAIL", "LoadingSpinner errors found in page")
                    return False
            else:
                self.log_test("Dashboard No Errors", "FAIL", f"Page returned {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard No Errors", "FAIL", f"Error loading page: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting LoadingSpinner Component Tests...")
        print("=" * 60)
        
        # Run tests
        tests = [
            self.test_server_status,
            self.test_signin_page_no_errors,
            self.test_signup_page_no_errors,
            self.test_forgot_password_no_errors,
            self.test_reset_password_no_errors,
            self.test_dashboard_no_errors
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
            print("🎉 All tests passed! LoadingSpinner component is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the results above.")
        
        return passed == total
    
    def save_results(self):
        """Save test results to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"loading_spinner_test_results_{timestamp}.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📄 Results saved to: {filepath}")

def main():
    """Main test function"""
    test = LoadingSpinnerTest()
    
    try:
        success = test.run_all_tests()
        test.save_results()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Test suite crashed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 