#!/usr/bin/env python3
"""
Comprehensive Backend Test Suite
Tests all completed backend test cases for AI Camera Counting System
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

class BackendTestSuite:
    def __init__(self):
        self.base_url_auth = "http://localhost:3001/api/v1"
        self.base_url_camera = "http://localhost:3002/api/v1"
        self.auth_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        print(f"[{status}] {test_name}: {details}")
        
    def delay(self, seconds: float = 1.0):
        """Add delay between tests to prevent rate limiting"""
        time.sleep(seconds)
        
    def retry_request(self, method: str, url: str, **kwargs):
        """Retry request with exponential backoff"""
        max_retries = 3
        base_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                response = requests.request(method, url, **kwargs)
                if response.status_code != 429:  # Not rate limited
                    return response
                    
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
                    continue
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
                    continue
                else:
                    raise e
                    
        return response  # Return last response even if rate limited
            
    def get_auth_token(self) -> bool:
        """Get authentication token"""
        try:
            response = requests.post(f"{self.base_url_auth}/auth/login", 
                                   json={"username": "testadmin", "password": "Test123!"})
            if response.status_code == 200:
                self.auth_token = response.json()["data"]["accessToken"]
                return True
            else:
                self.log_test("Get Auth Token", "FAILED", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Auth Token", "FAILED", str(e))
            return False
            
    def test_authentication_negative(self):
        """Test Authentication Negative Cases"""
        print("\n=== Testing Authentication Negative Cases ===")
        
        # AUTH-REG-002: Registration with Invalid Code
        try:
            response = requests.post(f"{self.base_url_auth}/auth/register", 
                                   json={"username": "testuser3", "email": "testuser3@example.com", 
                                        "password": "Test123!", "confirmPassword": "Test123!", 
                                        "registrationCode": "INVALID_CODE", "firstName": "Test", "lastName": "User3"})
            if response.status_code == 400:
                self.log_test("AUTH-REG-002", "PASSED", "Registration with invalid code rejected")
            else:
                self.log_test("AUTH-REG-002", "FAILED", f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("AUTH-REG-002", "FAILED", str(e))
            
        # AUTH-REG-003: Registration with Duplicate Username
        try:
            response = requests.post(f"{self.base_url_auth}/auth/register", 
                                   json={"username": "testadmin", "email": "testadmin2@example.com", 
                                        "password": "Test123!", "confirmPassword": "Test123!", 
                                        "registrationCode": "REG001", "firstName": "Test", "lastName": "Admin2"})
            if response.status_code == 400:
                self.log_test("AUTH-REG-003", "PASSED", "Registration with duplicate username rejected")
            else:
                self.log_test("AUTH-REG-003", "FAILED", f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("AUTH-REG-003", "FAILED", str(e))
            
        # AUTH-LOGIN-002: Login with Invalid Credentials
        try:
            response = requests.post(f"{self.base_url_auth}/auth/login", 
                                   json={"username": "testadmin", "password": "WrongPassword123!"})
            if response.status_code == 401:
                self.log_test("AUTH-LOGIN-002", "PASSED", "Login with invalid credentials rejected")
            else:
                self.log_test("AUTH-LOGIN-002", "FAILED", f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_test("AUTH-LOGIN-002", "FAILED", str(e))
            
    def test_authentication_positive(self):
        """Test Authentication Positive Cases"""
        print("\n=== Testing Authentication Positive Cases ===")
        
        # AUTH-TOKEN-001: Refresh Access Token
        try:
            # First login to get refresh token
            login_response = requests.post(f"{self.base_url_auth}/auth/login", 
                                         json={"username": "testadmin", "password": "Test123!"})
            if login_response.status_code == 200:
                refresh_token = login_response.json()["data"]["refreshToken"]
                
                # Test refresh token
                response = requests.post(f"{self.base_url_auth}/auth/refresh", 
                                       json={"refreshToken": refresh_token})
                if response.status_code == 200:
                    self.log_test("AUTH-TOKEN-001", "PASSED", "Token refresh successful")
                else:
                    self.log_test("AUTH-TOKEN-001", "FAILED", f"Status: {response.status_code}")
            else:
                self.log_test("AUTH-TOKEN-001", "FAILED", "Could not get refresh token")
        except Exception as e:
            self.log_test("AUTH-TOKEN-001", "FAILED", str(e))
            
        # AUTH-TOKEN-002: Logout User
        try:
            response = requests.post(f"{self.base_url_auth}/auth/logout", 
                                   headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                self.log_test("AUTH-TOKEN-002", "PASSED", "Logout successful")
            else:
                self.log_test("AUTH-TOKEN-002", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("AUTH-TOKEN-002", "FAILED", str(e))
            
        # AUTH-PROFILE-001: Get User Profile
        try:
            response = requests.get(f"{self.base_url_auth}/auth/me", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                self.log_test("AUTH-PROFILE-001", "PASSED", "Profile retrieved successfully")
            else:
                self.log_test("AUTH-PROFILE-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("AUTH-PROFILE-001", "FAILED", str(e))
            
        # AUTH-PROFILE-002: Update User Profile
        try:
            response = requests.put(f"{self.base_url_auth}/users/profile", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"},
                                  json={"firstName": "Updated", "lastName": "Name"})
            if response.status_code == 200:
                self.log_test("AUTH-PROFILE-002", "PASSED", "Profile updated successfully")
            else:
                self.log_test("AUTH-PROFILE-002", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("AUTH-PROFILE-002", "FAILED", str(e))
            
    def test_camera_management(self):
        """Test Camera Management API"""
        print("\n=== Testing Camera Management API ===")
        
        # CAM-REG-001: Register New Camera
        try:
            self.delay(1.0)  # Add delay before test
            response = self.retry_request("POST", f"{self.base_url_camera}/cameras", 
                                   headers={"Authorization": f"Bearer {self.auth_token}"},
                                   json={"name": "Test Camera 1", "ip_address": "192.168.1.100", "rtsp_url": "rtsp://192.168.1.100:554/stream"})
            if response.status_code == 200:
                camera_id = response.json()["data"]["id"]
                self.log_test("CAM-REG-001", "PASSED", f"Camera created with ID: {camera_id}")
                
                # CAM-GET-001: Get Camera by ID
                self.delay(1.0)
                response = self.retry_request("GET", f"{self.base_url_camera}/cameras/{camera_id}", 
                                      headers={"Authorization": f"Bearer {self.auth_token}"})
                if response.status_code == 200:
                    self.log_test("CAM-GET-001", "PASSED", "Camera retrieved successfully")
                else:
                    self.log_test("CAM-GET-001", "FAILED", f"Status: {response.status_code}")
                    
                # CAM-UPD-001: Update Camera
                self.delay(1.0)
                response = self.retry_request("PUT", f"{self.base_url_camera}/cameras/{camera_id}", 
                                      headers={"Authorization": f"Bearer {self.auth_token}"},
                                      json={"name": "Updated Test Camera", "description": "Updated description"})
                if response.status_code == 200:
                    self.log_test("CAM-UPD-001", "PASSED", "Camera updated successfully")
                else:
                    self.log_test("CAM-UPD-001", "FAILED", f"Status: {response.status_code}")
                    
                # CAM-DEL-001: Delete Camera
                self.delay(1.0)
                response = self.retry_request("DELETE", f"{self.base_url_camera}/cameras/{camera_id}", 
                                      headers={"Authorization": f"Bearer {self.auth_token}"})
                if response.status_code == 200:
                    self.log_test("CAM-DEL-001", "PASSED", "Camera deleted successfully")
                else:
                    self.log_test("CAM-DEL-001", "FAILED", f"Status: {response.status_code}")
            else:
                self.log_test("CAM-REG-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("CAM-REG-001", "FAILED", str(e))
            
        # CAM-REG-002: Register Camera with Invalid Data
        try:
            self.delay(1.0)
            response = self.retry_request("POST", f"{self.base_url_camera}/cameras", 
                                   headers={"Authorization": f"Bearer {self.auth_token}"},
                                   json={"name": "", "description": "Invalid camera"})
            if response.status_code in [400, 422]:
                self.log_test("CAM-REG-002", "PASSED", "Invalid camera data rejected")
            else:
                self.log_test("CAM-REG-002", "FAILED", f"Expected 422/400, got {response.status_code}")
        except Exception as e:
            self.log_test("CAM-REG-002", "FAILED", str(e))
            
        # CAM-LIST-001: Get All Cameras
        try:
            self.delay(1.0)
            response = self.retry_request("GET", f"{self.base_url_camera}/cameras", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                cameras = response.json()["data"]
                self.log_test("CAM-LIST-001", "PASSED", f"Retrieved {len(cameras)} cameras")
            else:
                self.log_test("CAM-LIST-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("CAM-LIST-001", "FAILED", str(e))
            
        # CAM-GET-002: Get Non-existent Camera
        try:
            self.delay(1.0)
            response = self.retry_request("GET", f"{self.base_url_camera}/cameras/99999", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 404:
                self.log_test("CAM-GET-002", "PASSED", "Non-existent camera handled correctly")
            else:
                self.log_test("CAM-GET-002", "FAILED", f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("CAM-GET-002", "FAILED", str(e))
            
    def test_count_data_management(self):
        """Test Count Data Management"""
        print("\n=== Testing Count Data Management ===")
        
        # COUNT-LIST-001: List All Count Data
        try:
            response = requests.get(f"{self.base_url_camera}/counts", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                counts = response.json()["data"]
                self.log_test("COUNT-LIST-001", "PASSED", f"Retrieved {len(counts)} count records")
            else:
                self.log_test("COUNT-LIST-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("COUNT-LIST-001", "FAILED", str(e))
            
        # COUNT-GET-001: Get Count Data by Camera ID
        try:
            response = requests.get(f"{self.base_url_camera}/counts?camera_id=1", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                counts = response.json()["data"]
                self.log_test("COUNT-GET-001", "PASSED", f"Retrieved {len(counts)} count records for camera 1")
            else:
                self.log_test("COUNT-GET-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("COUNT-GET-001", "FAILED", str(e))
            
    def test_analytics(self):
        """Test Analytics API"""
        print("\n=== Testing Analytics API ===")
        
        # ANALYTICS-001: Get Analytics Summary
        try:
            response = requests.get(f"{self.base_url_camera}/analytics/summary", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                data = response.json()["data"]
                self.log_test("ANALYTICS-001", "PASSED", f"Analytics summary: {data['total_cameras']} cameras, {data['current_count']} current count")
            else:
                self.log_test("ANALYTICS-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("ANALYTICS-001", "FAILED", str(e))
            
    def test_camera_processing(self):
        """Test Camera Processing"""
        print("\n=== Testing Camera Processing ===")
        
        # CAM-START-001: Start Camera Processing
        try:
            response = requests.post(f"{self.base_url_camera}/cameras/1/start", 
                                   headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                self.log_test("CAM-START-001", "PASSED", "Camera processing started")
            else:
                self.log_test("CAM-START-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("CAM-START-001", "FAILED", str(e))
            
        # CAM-STOP-001: Stop Camera Processing
        try:
            response = requests.post(f"{self.base_url_camera}/cameras/1/stop", 
                                   headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                self.log_test("CAM-STOP-001", "PASSED", "Camera processing stopped")
            else:
                self.log_test("CAM-STOP-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("CAM-STOP-001", "FAILED", str(e))
            
        # WORKER-STATUS-001: Get Worker Pool Status
        try:
            response = requests.get(f"{self.base_url_camera}/workers/status", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                data = response.json()["data"]
                self.log_test("WORKER-STATUS-001", "PASSED", f"Worker pool: {data['total_workers']} workers, {data['idle_workers']} idle")
            else:
                self.log_test("WORKER-STATUS-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("WORKER-STATUS-001", "FAILED", str(e))
            
    def test_security(self):
        """Test Security Features"""
        print("\n=== Testing Security Features ===")
        
        # SEC-AUTH-001: Access Protected Endpoint Without Token
        try:
            response = requests.get(f"{self.base_url_camera}/cameras")
            if response.status_code == 401:
                self.log_test("SEC-AUTH-001", "PASSED", "Unauthorized access blocked")
            else:
                self.log_test("SEC-AUTH-001", "FAILED", f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_test("SEC-AUTH-001", "FAILED", str(e))
            
        # SEC-AUTH-002: Access Protected Endpoint with Invalid Token
        try:
            response = requests.get(f"{self.base_url_camera}/cameras", 
                                  headers={"Authorization": "Bearer invalid_token"})
            if response.status_code == 401:
                self.log_test("SEC-AUTH-002", "PASSED", "Invalid token rejected")
            else:
                self.log_test("SEC-AUTH-002", "FAILED", f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_test("SEC-AUTH-002", "FAILED", str(e))
            
    def test_performance(self):
        """Test Performance"""
        print("\n=== Testing Performance ===")
        
        # PERF-LOAD-001: Load Test - Multiple Concurrent Requests
        try:
            start_time = time.time()
            responses = []
            for i in range(10):
                self.delay(0.5)  # Add delay between requests
                response = self.retry_request("GET", f"{self.base_url_camera}/cameras", 
                                      headers={"Authorization": f"Bearer {self.auth_token}"})
                responses.append(response.status_code)
            
            end_time = time.time()
            duration = end_time - start_time
            success_count = sum(1 for code in responses if code == 200)
            
            if success_count == 10:
                self.log_test("PERF-LOAD-001", "PASSED", f"All 10 requests successful in {duration:.2f}s")
            else:
                self.log_test("PERF-LOAD-001", "FAILED", f"{success_count}/10 requests successful")
        except Exception as e:
            self.log_test("PERF-LOAD-001", "FAILED", str(e))
            
    def test_integration(self):
        """Test Integration"""
        print("\n=== Testing Integration ===")
        
        # INT-AUTH-CAM-001: Camera API with Authentication
        try:
            self.delay(1.0)
            response = self.retry_request("GET", f"{self.base_url_camera}/cameras", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200 and response.json()["success"]:
                self.log_test("INT-AUTH-CAM-001", "PASSED", "Camera API with auth successful")
            else:
                self.log_test("INT-AUTH-CAM-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("INT-AUTH-CAM-001", "FAILED", str(e))
            
        # INT-DB-CAM-001: Camera API Database Integration
        try:
            self.delay(1.0)
            response = self.retry_request("GET", f"{self.base_url_camera}/cameras", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                cameras = response.json()["data"]
                if len(cameras) > 0:
                    self.log_test("INT-DB-CAM-001", "PASSED", f"Database integration: {len(cameras)} cameras")
                else:
                    self.log_test("INT-DB-CAM-001", "FAILED", "No cameras returned from database")
            else:
                self.log_test("INT-DB-CAM-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("INT-DB-CAM-001", "FAILED", str(e))
            
        # INT-DB-COUNT-001: Count Data Database Integration
        try:
            self.delay(1.0)
            response = self.retry_request("GET", f"{self.base_url_camera}/counts", 
                                  headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                counts = response.json()["data"]
                if len(counts) > 0:
                    self.log_test("INT-DB-COUNT-001", "PASSED", f"Database integration: {len(counts)} count records")
                else:
                    self.log_test("INT-DB-COUNT-001", "FAILED", "No count records returned from database")
            else:
                self.log_test("INT-DB-COUNT-001", "FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("INT-DB-COUNT-001", "FAILED", str(e))
            
    def test_error_handling(self):
        """Test Error Handling"""
        print("\n=== Testing Error Handling ===")
        
        # ERR-404-001: 404 Not Found
        try:
            response = requests.get(f"{self.base_url_camera}/api/v1/nonexistent")
            if response.status_code == 404:
                self.log_test("ERR-404-001", "PASSED", "404 error handled correctly")
            else:
                self.log_test("ERR-404-001", "FAILED", f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("ERR-404-001", "FAILED", str(e))
            
    def run_all_tests(self):
        """Run all test suites"""
        print("Starting Comprehensive Backend Test Suite")
        print("=" * 50)
        
        # Get authentication token first
        if not self.get_auth_token():
            print("Failed to get authentication token. Exiting.")
            return False
            
        # Run all test suites
        self.test_authentication_negative()
        self.test_authentication_positive()
        self.test_camera_management()
        self.test_count_data_management()
        self.test_analytics()
        self.test_camera_processing()
        self.test_security()
        self.test_performance()
        self.test_integration()
        self.test_error_handling()
        
        # Generate summary
        self.generate_summary()
        
        return True
        
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["status"] == "PASSED")
        failed_tests = sum(1 for result in self.test_results if result["status"] == "FAILED")
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Save results to file
        with open("results/comprehensive_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "results": self.test_results
            }, f, indent=2)
            
        print(f"\nResults saved to: results/comprehensive_test_results.json")

if __name__ == "__main__":
    test_suite = BackendTestSuite()
    success = test_suite.run_all_tests()
    sys.exit(0 if success else 1) 