#!/usr/bin/env python3
"""
🧪 Authentication API Tests - AI Camera Counting System
📅 Created: 2025-01-09
👥 Maintainer: QA Team

Test Cases: AUTH-001 to AUTH-010
Priority: High
Type: API Integration
"""

import requests
import json
import sys
import time
from datetime import datetime
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class AuthenticationAPITest:
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        self.config = self.load_config()
        self.base_url = self.config['test_environment']['base_urls']['auth_api']
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        self.last_registered_user = None  # NEW: lưu username vừa đăng ký
        self.last_registered_password = None  # NEW: lưu password vừa đăng ký
        
    def load_config(self):
        """Load test configuration"""
        config_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'config', 'test_config.json'
        )
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Test configuration file not found")
            sys.exit(1)
    
    def log_test(self, test_name, status, message, details=None):
        """Log test result"""
        result = {
            'test_name': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        
        # Print result
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {message}")
        
        if details:
            print(f"   Details: {details}")
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        test_name = "AUTH-001"
        
        try:
            # Health endpoint is at root level, not under /api/v1
            base_url = self.base_url.replace('/api/v1', '')
            response = self.session.get(f"{base_url}/health")
            
            if response.status_code == 200:
                self.log_test(
                    test_name,
                    "PASS",
                    "Health endpoint is accessible",
                    f"Status: {response.status_code}, Response: {response.json()}"
                )
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"Health endpoint failed with status {response.status_code}",
                    f"Response: {response.text}"
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(
                test_name,
                "FAIL",
                f"Health endpoint request failed: {str(e)}"
            )
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        test_name = "AUTH-002"
        try:
            # Test data
            timestamp = int(time.time())
            test_user = {
                "username": f"testuser{timestamp}",
                "email": f"testuser{timestamp}@example.com",
                "password": "Test123!",
                "confirmPassword": "Test123!",
                "firstName": "Test",
                "lastName": "User",
                "registrationCode": "REG001"
            }
            response = self.session.post(
                f"{self.base_url}/auth/register",
                json=test_user
            )
            if response.status_code == 201:
                self.log_test(
                    test_name,
                    "PASS",
                    "User registration successful",
                    f"Status: {response.status_code}, User: {test_user['username']}"
                )
                # Lưu lại user vừa đăng ký để test login
                self.last_registered_user = test_user["username"]
                self.last_registered_password = test_user["password"]
                # Lấy token từ response đăng ký
                resp_json = response.json()
                if 'data' in resp_json:
                    self.access_token = resp_json['data'].get('accessToken')
                    self.refresh_token = resp_json['data'].get('refreshToken')
                    print(f"DEBUG: access_token = {self.access_token}")
                    print(f"DEBUG: refresh_token = {self.refresh_token}")
                # Đăng nhập user mới để lấy token (dự phòng)
                if not self.access_token or not self.refresh_token:
                    login_resp = self.session.post(
                        f"{self.base_url}/auth/login",
                        json={
                            "username": test_user["username"],
                            "password": test_user["password"]
                        }
                    )
                    if login_resp.status_code == 200:
                        data = login_resp.json()
                        if 'data' in data:
                            self.access_token = data['data'].get('accessToken') or data['data'].get('access_token')
                            self.refresh_token = data['data'].get('refreshToken') or data['data'].get('refresh_token')
                        else:
                            self.access_token = data.get('accessToken') or data.get('access_token')
                            self.refresh_token = data.get('refreshToken') or data.get('refresh_token')
                        print(f"DEBUG: access_token from login = {self.access_token}")
                        print(f"DEBUG: refresh_token from login = {self.refresh_token}")
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"User registration failed with status {response.status_code}",
                    f"Response: {response.text}"
                )
                return False
        except requests.exceptions.RequestException as e:
            self.log_test(
                test_name,
                "FAIL",
                f"User registration request failed: {str(e)}"
            )
            return False
    
    def test_user_login(self):
        """Test user login"""
        test_name = "AUTH-003"
        try:
            # Sử dụng user vừa đăng ký nếu có, nếu không fallback về admin
            if self.last_registered_user and self.last_registered_password:
                username = self.last_registered_user
                password = self.last_registered_password
            else:
                admin_creds = self.config['test_users']['admin']
                username = admin_creds['username']
                password = admin_creds['password']
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": username,
                    "password": password
                }
            )
            if response.status_code == 200:
                self.log_test(
                    test_name,
                    "PASS",
                    "User login successful",
                    f"Status: {response.status_code}, User: {username}"
                )
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"User login failed with status {response.status_code}",
                    f"Response: {response.text}"
                )
                return False
        except requests.exceptions.RequestException as e:
            self.log_test(
                test_name,
                "FAIL",
                f"User login request failed: {str(e)}"
            )
            return False
    
    def test_protected_endpoint(self):
        """Test protected endpoint access"""
        test_name = "AUTH-004"
        print(f"DEBUG: test_protected_endpoint - access_token = {self.access_token}")
        if not self.access_token:
            self.log_test(
                test_name,
                "SKIP",
                "No access token available for protected endpoint test (user registration/login may have failed)"
            )
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = self.session.get(
                f"{self.base_url}/users/profile",
                headers=headers
            )
            if response.status_code == 200:
                self.log_test(
                    test_name,
                    "PASS",
                    "Protected endpoint accessible with valid token",
                    f"Status: {response.status_code}"
                )
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"Protected endpoint failed with status {response.status_code}",
                    f"Response: {response.text}"
                )
                return False
        except requests.exceptions.RequestException as e:
            self.log_test(
                test_name,
                "FAIL",
                f"Protected endpoint request failed: {str(e)}"
            )
            return False

    def test_token_refresh(self):
        """Test token refresh"""
        test_name = "AUTH-005"
        print(f"DEBUG: test_token_refresh - refresh_token = {self.refresh_token}")
        if not self.refresh_token:
            self.log_test(
                test_name,
                "SKIP",
                "No refresh token available for refresh test (user registration/login may have failed)"
            )
            return False
        try:
            response = self.session.post(
                f"{self.base_url}/auth/refresh",
                json={"refreshToken": self.refresh_token}
            )
            if response.status_code == 200:
                data = response.json()
                new_access_token = None
                if 'data' in data:
                    new_access_token = data['data'].get('accessToken') or data['data'].get('access_token')
                else:
                    new_access_token = data.get('accessToken') or data.get('access_token')
                if new_access_token:
                    self.access_token = new_access_token
                    self.log_test(
                        test_name,
                        "PASS",
                        "Token refresh successful",
                        f"Status: {response.status_code}"
                    )
                    return True
                else:
                    self.log_test(
                        test_name,
                        "FAIL",
                        "Token refresh response missing access_token",
                        f"Response: {response.text}"
                    )
                    return False
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"Token refresh failed with status {response.status_code}",
                    f"Response: {response.text}"
                )
                return False
        except requests.exceptions.RequestException as e:
            self.log_test(
                test_name,
                "FAIL",
                f"Token refresh request failed: {str(e)}"
            )
            return False

    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        test_name = "AUTH-006"
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": "invalid_user",
                    "password": "invalid_password"
                }
            )
            
            if response.status_code == 401:
                self.log_test(
                    test_name,
                    "PASS",
                    "Invalid credentials properly rejected",
                    f"Status: {response.status_code}"
                )
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"Invalid credentials not properly rejected, status: {response.status_code}",
                    f"Response: {response.text}"
                )
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(
                test_name,
                "FAIL",
                f"Invalid credentials test request failed: {str(e)}"
            )
            return False
    
    def test_logout(self):
        """Test user logout"""
        test_name = "AUTH-007"
        print(f"DEBUG: test_logout - access_token = {self.access_token}")
        if not self.access_token:
            self.log_test(
                test_name,
                "SKIP",
                "No access token available for logout test (user registration/login may have failed)"
            )
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = self.session.post(
                f"{self.base_url}/auth/logout",
                headers=headers
            )
            if response.status_code == 200:
                self.log_test(
                    test_name,
                    "PASS",
                    "User logout successful",
                    f"Status: {response.status_code}"
                )
                return True
            else:
                self.log_test(
                    test_name,
                    "FAIL",
                    f"User logout failed with status {response.status_code}",
                    f"Response: {response.text}"
                )
                return False
        except requests.exceptions.RequestException as e:
            self.log_test(
                test_name,
                "FAIL",
                f"User logout request failed: {str(e)}"
            )
            return False
    
    def save_results(self):
        """Save test results to file"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        results = {
            'test_suite': 'Authentication API Tests',
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': duration,
            'total_tests': len(self.test_results),
            'passed_tests': len([r for r in self.test_results if r['status'] == 'PASS']),
            'failed_tests': len([r for r in self.test_results if r['status'] == 'FAIL']),
            'results': self.test_results
        }
        
        # Create results directory if it doesn't exist
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        # Save JSON results
        results_file = os.path.join(results_dir, 'auth_api_test_results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Results saved to: {results_file}")
        
        return results
    
    def run_all_tests(self):
        """Run all authentication tests"""
        print("==========================================")
        print("🧪 AUTHENTICATION API TESTS")
        print("AI Camera Counting System")
        print("==========================================")
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Run tests tuần tự, giữ nguyên self
        passed = 0
        total = 0
        for test in [
            self.test_health_endpoint,
            self.test_user_registration,
            self.test_user_login,
            self.test_protected_endpoint,
            self.test_token_refresh,
            self.test_invalid_credentials,
            self.test_logout
        ]:
            total += 1
            if test():
                passed += 1
        # Summary
        print("")
        print("==========================================")
        print("📊 TEST SUMMARY")
        print("==========================================")
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        if passed == total:
            print("🎉 All authentication tests passed!")
        else:
            print("⚠️  Some authentication tests failed!")
        # Save results
        results = self.save_results()
        return passed == total

def main():
    """Main function"""
    try:
        test_suite = AuthenticationAPITest()
        success = test_suite.run_all_tests()
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 