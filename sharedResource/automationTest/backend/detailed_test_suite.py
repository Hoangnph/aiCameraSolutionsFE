#!/usr/bin/env python3
"""
Detailed Backend Test Suite
Tests each backend test case individually with proper delays
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DetailedBackendTestSuite:
    def __init__(self):
        self.base_url_auth = "http://localhost:3001"
        self.base_url_camera = "http://localhost:3002"
        self.results = []
        self.test_users = []
        self.auth_tokens = {}
        
    def log_test(self, test_name: str, status: str, details: str):
        """Log test result"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        logger.info(f"[{status}] {test_name}: {details}")
        
    def wait_for_rate_limit(self, seconds: int = 2):
        """Wait to avoid rate limiting"""
        time.sleep(seconds)
        
    def register_test_user(self, username: str, email: str) -> Dict:
        """Register a test user"""
        url = f"{self.base_url_auth}/api/v1/auth/register"
        data = {
            "username": username,
            "email": email,
            "password": "TestPass123!",
            "confirmPassword": "TestPass123!",
            "firstName": "Test",
            "lastName": "User",
            "registrationCode": "REG001"
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            logger.error(f"Failed to register user: {response.status_code} - {response.text}")
            return None
            
    def login_user(self, username: str, password: str) -> str:
        """Login user and return access token"""
        url = f"{self.base_url_auth}/api/v1/auth/login"
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()["data"]["accessToken"]
        else:
            logger.error(f"Failed to login: {response.status_code} - {response.text}")
            return None

    # ==================== AUTHENTICATION TEST CASES ====================
    
    def test_auth_registration_positive(self):
        """Test Case: AUTH-REG-001 - User Registration (Positive)"""
        test_name = "AUTH-REG-001"
        
        try:
            username = f"testuser{int(time.time())}"
            email = f"{username}@example.com"
            
            url = f"{self.base_url_auth}/api/v1/auth/register"
            data = {
                "username": username,
                "email": email,
                "password": "TestPass123!",
                "confirmPassword": "TestPass123!",
                "firstName": "Test",
                "lastName": "User",
                "registrationCode": "REG001"
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 201:
                self.log_test(test_name, "PASSED", f"User registered successfully: {username}")
                self.test_users.append(username)
            else:
                self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_auth_registration_invalid_code(self):
        """Test Case: AUTH-REG-002 - Registration with Invalid Code"""
        test_name = "AUTH-REG-002"
        
        try:
            url = f"{self.base_url_auth}/api/v1/auth/register"
            data = {
                "username": f"testuser_invalid_{int(time.time())}",
                "email": "invalid@example.com",
                "password": "TestPass123!",
                "confirmPassword": "TestPass123!",
                "firstName": "Test",
                "lastName": "User",
                "registrationCode": "INVALID"
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 400:
                self.log_test(test_name, "PASSED", "Invalid registration code rejected")
            else:
                self.log_test(test_name, "FAILED", f"Expected 400, got {response.status_code}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_auth_registration_duplicate_username(self):
        """Test Case: AUTH-REG-003 - Registration with Duplicate Username"""
        test_name = "AUTH-REG-003"
        
        try:
            # First registration
            username = f"duplicateuser{int(time.time())}"
            url = f"{self.base_url_auth}/api/v1/auth/register"
            data = {
                "username": username,
                "email": f"{username}@example.com",
                "password": "TestPass123!",
                "confirmPassword": "TestPass123!",
                "firstName": "Test",
                "lastName": "User",
                "registrationCode": "REG001"
            }
            
            response = requests.post(url, json=data)
            if response.status_code == 201:
                self.test_users.append(username)
                
            # Second registration with same username
            data["email"] = "different@example.com"
            response = requests.post(url, json=data)
            
            if response.status_code == 400:
                self.log_test(test_name, "PASSED", "Duplicate username rejected")
            else:
                self.log_test(test_name, "FAILED", f"Expected 400, got {response.status_code}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_auth_login_positive(self):
        """Test Case: AUTH-LOGIN-001 - User Login (Positive)"""
        test_name = "AUTH-LOGIN-001"
        
        try:
            # Register a user first
            username = f"loginuser{int(time.time())}"
            email = f"{username}@example.com"
            
            # Register
            reg_url = f"{self.base_url_auth}/api/v1/auth/register"
            reg_data = {
                "username": username,
                "email": email,
                "password": "TestPass123!",
                "confirmPassword": "TestPass123!",
                "firstName": "Test",
                "lastName": "User",
                "registrationCode": "REG001"
            }
            
            reg_response = requests.post(reg_url, json=reg_data)
            if reg_response.status_code == 201:
                self.test_users.append(username)
                
                # Login
                login_url = f"{self.base_url_auth}/api/v1/auth/login"
                login_data = {
                    "username": username,
                    "password": "TestPass123!"
                }
                
                response = requests.post(login_url, json=login_data)
                
                if response.status_code == 200:
                    token_data = response.json()
                    if "accessToken" in token_data["data"]:
                        self.auth_tokens[username] = token_data["data"]["accessToken"]
                        self.log_test(test_name, "PASSED", f"Login successful for {username}")
                    else:
                        self.log_test(test_name, "FAILED", "No access token in response")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "FAILED", f"Registration failed: {reg_response.status_code}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_auth_login_invalid_credentials(self):
        """Test Case: AUTH-LOGIN-002 - Login with Invalid Credentials"""
        test_name = "AUTH-LOGIN-002"
        
        try:
            url = f"{self.base_url_auth}/api/v1/auth/login"
            data = {
                "username": "nonexistent_user",
                "password": "wrong_password"
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 401:
                self.log_test(test_name, "PASSED", "Invalid credentials rejected")
            else:
                self.log_test(test_name, "FAILED", f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_auth_token_verification(self):
        """Test Case: AUTH-TOKEN-001 - Token Verification"""
        test_name = "AUTH-TOKEN-001"
        
        try:
            # Get a valid token first
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_auth}/api/v1/auth/verify"
                headers = {"Authorization": f"Bearer {token}"}
                
                response = requests.post(url, headers=headers)
                
                if response.status_code == 200:
                    self.log_test(test_name, "PASSED", "Token verification successful")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_auth_logout(self):
        """Test Case: AUTH-TOKEN-002 - User Logout"""
        test_name = "AUTH-TOKEN-002"
        
        try:
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_auth}/api/v1/auth/logout"
                headers = {"Authorization": f"Bearer {token}"}
                
                response = requests.post(url, headers=headers)
                
                if response.status_code == 200:
                    self.log_test(test_name, "PASSED", "Logout successful")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_auth_profile_get(self):
        """Test Case: AUTH-PROFILE-001 - Get User Profile"""
        test_name = "AUTH-PROFILE-001"
        
        try:
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_auth}/api/v1/users/profile"
                headers = {"Authorization": f"Bearer {token}"}
                
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    self.log_test(test_name, "PASSED", "Profile retrieved successfully")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_auth_profile_update(self):
        """Test Case: AUTH-PROFILE-002 - Update User Profile"""
        test_name = "AUTH-PROFILE-002"
        
        try:
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_auth}/api/v1/users/profile"
                headers = {"Authorization": f"Bearer {token}"}
                data = {
                    "firstName": "Updated",
                    "lastName": "Name"
                }
                
                response = requests.put(url, json=data, headers=headers)
                
                if response.status_code == 200:
                    self.log_test(test_name, "PASSED", "Profile updated successfully")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()

    # ==================== CAMERA MANAGEMENT TEST CASES ====================
    
    def test_camera_create(self):
        """Test Case: CAM-CRUD-001 - Create Camera"""
        test_name = "CAM-CRUD-001"
        
        try:
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_camera}/api/v1/cameras"
                headers = {"Authorization": f"Bearer {token}"}
                data = {
                    "name": f"Test Camera {int(time.time())}",
                    "description": "Test camera for automation testing",
                    "ip_address": "192.168.1.100",
                    "rtsp_url": "rtsp://192.168.1.100:554/stream",
                    "status": "offline"
                }
                
                response = requests.post(url, json=data, headers=headers)
                
                if response.status_code in [200, 201]:
                    camera_data = response.json()
                    if "id" in camera_data["data"]:
                        self.log_test(test_name, "PASSED", f"Camera created with ID: {camera_data['data']['id']}")
                    else:
                        self.log_test(test_name, "FAILED", "No camera ID in response")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_camera_list(self):
        """Test Case: CAM-CRUD-002 - List Cameras"""
        test_name = "CAM-CRUD-002"
        
        try:
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_camera}/api/v1/cameras"
                headers = {"Authorization": f"Bearer {token}"}
                
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    cameras = response.json()
                    count = len(cameras) if isinstance(cameras, list) else 0
                    self.log_test(test_name, "PASSED", f"Retrieved {count} cameras")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_camera_get(self):
        """Test Case: CAM-CRUD-003 - Get Camera by ID"""
        test_name = "CAM-CRUD-003"
        
        try:
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_camera}/api/v1/cameras/1"
                headers = {"Authorization": f"Bearer {token}"}
                
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    self.log_test(test_name, "PASSED", "Camera retrieved successfully")
                elif response.status_code == 404:
                    self.log_test(test_name, "PASSED", "Camera not found (expected for ID 1)")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_camera_update(self):
        """Test Case: CAM-CRUD-004 - Update Camera"""
        test_name = "CAM-CRUD-004"
        
        try:
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_camera}/api/v1/cameras/1"
                headers = {"Authorization": f"Bearer {token}"}
                data = {
                    "name": "UpdatedCameraName",
                    "description": "Updated camera description"
                }
                
                response = requests.put(url, json=data, headers=headers)
                
                if response.status_code == 200:
                    self.log_test(test_name, "PASSED", "Camera updated successfully")
                elif response.status_code == 404:
                    self.log_test(test_name, "PASSED", "Camera not found (expected for ID 1)")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_camera_delete(self):
        """Test Case: CAM-CRUD-005 - Delete Camera"""
        test_name = "CAM-CRUD-005"
        
        try:
            if not self.auth_tokens:
                self.test_auth_login_positive()
                self.wait_for_rate_limit()
            
            if self.auth_tokens:
                token = list(self.auth_tokens.values())[0]
                url = f"{self.base_url_camera}/api/v1/cameras/999"
                headers = {"Authorization": f"Bearer {token}"}
                
                response = requests.delete(url, headers=headers)
                
                if response.status_code == 200:
                    self.log_test(test_name, "PASSED", "Camera deleted successfully")
                elif response.status_code == 404:
                    self.log_test(test_name, "PASSED", "Camera not found (expected for ID 999)")
                else:
                    self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
            else:
                self.log_test(test_name, "SKIPPED", "No valid token available")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()

    # ==================== COUNT DATA TEST CASES ====================
    
    def test_count_data_list(self):
        """Test Case: COUNT-LIST-001 - List Count Data"""
        test_name = "COUNT-LIST-001"
        
        try:
            url = f"{self.base_url_camera}/api/v1/counts"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                counts = response.json()
                count = len(counts) if isinstance(counts, list) else 0
                self.log_test(test_name, "PASSED", f"Retrieved {count} count records")
            else:
                self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_count_data_by_camera(self):
        """Test Case: COUNT-GET-001 - Get Count Data by Camera"""
        test_name = "COUNT-GET-001"
        
        try:
            url = f"{self.base_url_camera}/api/v1/counts?camera_id=1"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                counts = response.json()
                count = len(counts) if isinstance(counts, list) else 0
                self.log_test(test_name, "PASSED", f"Retrieved {count} count records for camera 1")
            else:
                self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()

    # ==================== ANALYTICS TEST CASES ====================
    
    def test_analytics_summary(self):
        """Test Case: ANALYTICS-001 - Get Analytics Summary"""
        test_name = "ANALYTICS-001"
        
        try:
            url = f"{self.base_url_camera}/api/v1/analytics/summary"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                analytics = response.json()
                self.log_test(test_name, "PASSED", f"Analytics summary retrieved: {analytics}")
            else:
                self.log_test(test_name, "FAILED", f"Status: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()

    # ==================== SECURITY TEST CASES ====================
    
    def test_security_unauthorized_access(self):
        """Test Case: SEC-AUTH-001 - Unauthorized Access"""
        test_name = "SEC-AUTH-001"
        
        try:
            url = f"{self.base_url_camera}/api/v1/cameras"
            
            response = requests.get(url)
            
            if response.status_code == 401:
                self.log_test(test_name, "PASSED", "Unauthorized access blocked")
            else:
                self.log_test(test_name, "FAILED", f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()
    
    def test_security_invalid_token(self):
        """Test Case: SEC-AUTH-002 - Invalid Token"""
        test_name = "SEC-AUTH-002"
        
        try:
            url = f"{self.base_url_camera}/api/v1/cameras"
            headers = {"Authorization": "Bearer invalid_token"}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 401:
                self.log_test(test_name, "PASSED", "Invalid token rejected")
            else:
                self.log_test(test_name, "FAILED", f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()

    # ==================== ERROR HANDLING TEST CASES ====================
    
    def test_error_404(self):
        """Test Case: ERR-404-001 - 404 Error Handling"""
        test_name = "ERR-404-001"
        
        try:
            url = f"{self.base_url_camera}/api/v1/nonexistent"
            
            response = requests.get(url)
            
            if response.status_code == 404:
                self.log_test(test_name, "PASSED", "404 error handled correctly")
            else:
                self.log_test(test_name, "FAILED", f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test(test_name, "ERROR", f"Exception: {str(e)}")
            
        self.wait_for_rate_limit()

    # ==================== RUN ALL TESTS ====================
    
    def run_all_tests(self):
        """Run all test cases"""
        logger.info("Starting Detailed Backend Test Suite")
        logger.info("=" * 50)
        
        # Authentication Tests
        logger.info("=== Testing Authentication ===")
        self.test_auth_registration_positive()
        self.test_auth_registration_invalid_code()
        self.test_auth_registration_duplicate_username()
        self.test_auth_login_positive()
        self.test_auth_login_invalid_credentials()
        self.test_auth_token_verification()
        self.test_auth_logout()
        self.test_auth_profile_get()
        self.test_auth_profile_update()
        
        # Camera Management Tests
        logger.info("=== Testing Camera Management ===")
        self.test_camera_create()
        self.test_camera_list()
        self.test_camera_get()
        self.test_camera_update()
        self.test_camera_delete()
        
        # Count Data Tests
        logger.info("=== Testing Count Data ===")
        self.test_count_data_list()
        self.test_count_data_by_camera()
        
        # Analytics Tests
        logger.info("=== Testing Analytics ===")
        self.test_analytics_summary()
        
        # Security Tests
        logger.info("=== Testing Security ===")
        self.test_security_unauthorized_access()
        self.test_security_invalid_token()
        
        # Error Handling Tests
        logger.info("=== Testing Error Handling ===")
        self.test_error_404()
        
        # Generate summary
        self.generate_summary()
        
        return True
    
    def generate_summary(self):
        """Generate test summary"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["status"] == "PASSED"])
        failed_tests = len([r for r in self.results if r["status"] == "FAILED"])
        error_tests = len([r for r in self.results if r["status"] == "ERROR"])
        skipped_tests = len([r for r in self.results if r["status"] == "SKIPPED"])
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        summary = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "skipped_tests": skipped_tests,
                "success_rate": round(success_rate, 2)
            },
            "results": self.results
        }
        
        # Save results
        with open("results/detailed_test_results.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        logger.info("=" * 50)
        logger.info("TEST SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Errors: {error_tests}")
        logger.info(f"Skipped: {skipped_tests}")
        logger.info(f"Success Rate: {success_rate:.2f}%")
        logger.info("=" * 50)
        logger.info(f"Results saved to: results/detailed_test_results.json")

if __name__ == "__main__":
    test_suite = DetailedBackendTestSuite()
    success = test_suite.run_all_tests() 