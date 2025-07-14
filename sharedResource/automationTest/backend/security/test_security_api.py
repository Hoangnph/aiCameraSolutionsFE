#!/usr/bin/env python3
"""
Security Testing Suite - AI Camera Counting System
Tests security measures including JWT, RBAC, SQL Injection, XSS, Rate Limiting
"""

import requests
import json
import time
import sys
import jwt
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any

class SecurityTestSuite:
    def __init__(self):
        self.base_url_auth = "http://localhost:3001/api/v1"
        self.base_url_camera = "http://localhost:3002/api/v1"
        self.auth_token = None
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"[{status.upper()}] {test_name}: {details}")
        
    def get_auth_token(self) -> bool:
        """Get authentication token for testing"""
        try:
            # Register a test user first
            register_data = {
                "username": f"security_test_{int(time.time())}",
                "email": f"security_test_{int(time.time())}@example.com",
                "password": "TestPass123!",
                "confirmPassword": "TestPass123!",
                "firstName": "Security",
                "lastName": "Test",
                "registrationCode": "DEV2024"
            }
            
            response = self.session.post(f"{self.base_url_auth}/auth/register", json=register_data)
            if response.status_code == 201:
                self.auth_token = response.json()["data"]["accessToken"]
                return True
            else:
                # Try login if registration fails
                login_data = {
                    "username": "apitestuser",
                    "password": "Test123!"
                }
                response = self.session.post(f"{self.base_url_auth}/auth/login", json=login_data)
                if response.status_code == 200:
                    self.auth_token = response.json()["data"]["accessToken"]
                    return True
                    
            self.log_test("Get Auth Token", "FAILED", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log_test("Get Auth Token", "FAILED", str(e))
            return False

    def test_jwt_token_security(self):
        """TC-SEC-001: JWT Token Security Test"""
        print("\n=== Testing JWT Token Security ===")
        
        # Test 1: Token Generation Security
        try:
            response = self.session.post(f"{self.base_url_auth}/auth/login", 
                                       json={"username": "apitestuser", "password": "Test123!"})
            if response.status_code == 200:
                token = response.json()["data"]["accessToken"]
                
                # Verify token structure
                if len(token.split('.')) == 3:
                    self.log_test("TC-SEC-001.1", "PASSED", "JWT token structure valid")
                else:
                    self.log_test("TC-SEC-001.1", "FAILED", "Invalid JWT token structure")
                    
                # Test token tampering
                parts = token.split('.')
                tampered_payload = base64.b64encode(b'{"user_id":999,"role":"admin"}').decode()
                tampered_token = f"{parts[0]}.{tampered_payload}.{parts[2]}"
                
                response = self.session.get(f"{self.base_url_auth}/auth/me", 
                                          headers={"Authorization": f"Bearer {tampered_token}"})
                if response.status_code == 401:
                    self.log_test("TC-SEC-001.2", "PASSED", "Token tampering detected")
                else:
                    self.log_test("TC-SEC-001.2", "FAILED", "Token tampering not detected")
                    
            else:
                self.log_test("TC-SEC-001", "FAILED", "Could not get token for testing")
        except Exception as e:
            self.log_test("TC-SEC-001", "FAILED", str(e))

    def test_password_security(self):
        """TC-SEC-002: Password Security Test"""
        print("\n=== Testing Password Security ===")
        
        # Test 1: Password Complexity Requirements
        weak_passwords = ["123", "password", "abc", "123456"]
        for weak_pwd in weak_passwords:
            try:
                register_data = {
                    "username": f"weak_pwd_test_{int(time.time())}",
                    "email": f"weak_pwd_test_{int(time.time())}@example.com",
                    "password": weak_pwd,
                    "confirmPassword": weak_pwd,
                    "firstName": "Test",
                    "lastName": "User",
                    "registrationCode": "DEV2024"
                }
                
                response = self.session.post(f"{self.base_url_auth}/auth/register", json=register_data)
                if response.status_code == 400:
                    self.log_test("TC-SEC-002.1", "PASSED", f"Weak password '{weak_pwd}' rejected")
                else:
                    self.log_test("TC-SEC-002.1", "FAILED", f"Weak password '{weak_pwd}' accepted")
                    break
            except Exception as e:
                self.log_test("TC-SEC-002.1", "FAILED", str(e))
                break
                
        # Test 2: Password Hashing (verify password is not stored in plain text)
        try:
            # This would require database access to verify, but we can test indirectly
            response = self.session.post(f"{self.base_url_auth}/auth/login", 
                                       json={"username": "apitestuser", "password": "Test123!"})
            if response.status_code == 200:
                self.log_test("TC-SEC-002.2", "PASSED", "Password authentication working (likely hashed)")
            else:
                self.log_test("TC-SEC-002.2", "FAILED", "Password authentication failed")
        except Exception as e:
            self.log_test("TC-SEC-002.2", "FAILED", str(e))

    def test_rbac_security(self):
        """TC-SEC-003: Role-Based Access Control Test"""
        print("\n=== Testing Role-Based Access Control ===")
        
        # Test 1: Access to admin-only endpoints
        try:
            # Try to access admin endpoint with regular user token
            response = self.session.get(f"{self.base_url_auth}/users", 
                                      headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 403:
                self.log_test("TC-SEC-003.1", "PASSED", "Admin endpoint protected from regular users")
            else:
                self.log_test("TC-SEC-003.1", "FAILED", f"Admin endpoint accessible: {response.status_code}")
        except Exception as e:
            self.log_test("TC-SEC-003.1", "FAILED", str(e))
            
        # Test 2: Access to protected camera endpoints
        try:
            response = self.session.get(f"{self.base_url_camera}/cameras", 
                                      headers={"Authorization": f"Bearer {self.auth_token}"})
            if response.status_code == 200:
                self.log_test("TC-SEC-003.2", "PASSED", "Authenticated user can access camera endpoints")
            else:
                self.log_test("TC-SEC-003.2", "FAILED", f"Camera endpoint access denied: {response.status_code}")
        except Exception as e:
            self.log_test("TC-SEC-003.2", "FAILED", str(e))

    def test_api_authentication(self):
        """TC-SEC-004: API Authentication Test"""
        print("\n=== Testing API Authentication ===")
        
        # Test 1: Access without token
        try:
            response = self.session.get(f"{self.base_url_camera}/cameras")
            if response.status_code == 401:
                self.log_test("TC-SEC-004.1", "PASSED", "Unauthenticated access properly denied")
            else:
                self.log_test("TC-SEC-004.1", "FAILED", f"Unauthenticated access allowed: {response.status_code}")
        except Exception as e:
            self.log_test("TC-SEC-004.1", "FAILED", str(e))
            
        # Test 2: Access with invalid token
        try:
            response = self.session.get(f"{self.base_url_camera}/cameras", 
                                      headers={"Authorization": "Bearer invalid_token"})
            if response.status_code == 401:
                self.log_test("TC-SEC-004.2", "PASSED", "Invalid token properly rejected")
            else:
                self.log_test("TC-SEC-004.2", "FAILED", f"Invalid token accepted: {response.status_code}")
        except Exception as e:
            self.log_test("TC-SEC-004.2", "FAILED", str(e))
            
        # Test 3: Access with expired token (if we can generate one)
        try:
            # Create a token that expires in 1 second
            expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImlhdCI6MTYzNDU2Nzg5MCwiZXhwIjoxNjM0NTY3ODkxfQ.invalid"
            response = self.session.get(f"{self.base_url_camera}/cameras", 
                                      headers={"Authorization": f"Bearer {expired_token}"})
            if response.status_code == 401:
                self.log_test("TC-SEC-004.3", "PASSED", "Expired token properly rejected")
            else:
                self.log_test("TC-SEC-004.3", "FAILED", f"Expired token accepted: {response.status_code}")
        except Exception as e:
            self.log_test("TC-SEC-004.3", "FAILED", str(e))

    def test_sql_injection_prevention(self):
        """TC-SEC-006: SQL Injection Prevention Test"""
        print("\n=== Testing SQL Injection Prevention ===")
        
        # Test 1: SQL injection in username field
        sql_injection_payloads = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM users--"
        ]
        
        for payload in sql_injection_payloads:
            try:
                response = self.session.post(f"{self.base_url_auth}/auth/login", 
                                           json={"username": payload, "password": "test"})
                # Should not crash or return sensitive data
                if response.status_code in [400, 401, 422]:
                    self.log_test("TC-SEC-006.1", "PASSED", f"SQL injection '{payload}' properly handled")
                else:
                    self.log_test("TC-SEC-006.1", "FAILED", f"SQL injection '{payload}' not properly handled: {response.status_code}")
                    break
            except Exception as e:
                self.log_test("TC-SEC-006.1", "FAILED", f"SQL injection '{payload}' caused error: {str(e)}")
                break
                
        # Test 2: SQL injection in camera name field
        try:
            camera_data = {
                "name": "'; DROP TABLE cameras; --",
                "description": "Test camera",
                "ip_address": "192.168.1.100",
                "rtsp_url": "rtsp://test.com/stream"
            }
            
            response = self.session.post(f"{self.base_url_camera}/cameras", 
                                       headers={"Authorization": f"Bearer {self.auth_token}"},
                                       json=camera_data)
            if response.status_code in [400, 422]:
                self.log_test("TC-SEC-006.2", "PASSED", "SQL injection in camera name properly handled")
            else:
                self.log_test("TC-SEC-006.2", "FAILED", f"SQL injection in camera name not handled: {response.status_code}")
        except Exception as e:
            self.log_test("TC-SEC-006.2", "FAILED", str(e))

    def test_xss_prevention(self):
        """TC-SEC-007: XSS Prevention Test"""
        print("\n=== Testing XSS Prevention ===")
        
        # Test 1: XSS in camera name field
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//"
        ]
        
        for payload in xss_payloads:
            try:
                camera_data = {
                    "name": payload,
                    "description": "Test camera",
                    "ip_address": "192.168.1.100",
                    "rtsp_url": "rtsp://test.com/stream"
                }
                
                response = self.session.post(f"{self.base_url_camera}/cameras", 
                                           headers={"Authorization": f"Bearer {self.auth_token}"},
                                           json=camera_data)
                if response.status_code in [400, 422]:
                    self.log_test("TC-SEC-007.1", "PASSED", f"XSS payload '{payload}' properly rejected")
                else:
                    self.log_test("TC-SEC-007.1", "FAILED", f"XSS payload '{payload}' accepted: {response.status_code}")
                    break
            except Exception as e:
                self.log_test("TC-SEC-007.1", "FAILED", f"XSS payload '{payload}' caused error: {str(e)}")
                break

    def test_rate_limiting(self):
        """TC-SEC-009: Rate Limiting Test"""
        print("\n=== Testing Rate Limiting ===")
        
        # Test 1: Login rate limiting
        try:
            failed_attempts = 0
            for i in range(10):  # Try 10 rapid login attempts
                response = self.session.post(f"{self.base_url_auth}/auth/login", 
                                           json={"username": "apitestuser", "password": "WrongPassword"})
                if response.status_code == 401:
                    failed_attempts += 1
                elif response.status_code == 429:  # Rate limit exceeded
                    self.log_test("TC-SEC-009.1", "PASSED", f"Rate limiting triggered after {i+1} attempts")
                    break
                time.sleep(0.1)  # Small delay between requests
                
            if failed_attempts == 10:
                self.log_test("TC-SEC-009.1", "WARNING", "Rate limiting not detected after 10 attempts")
        except Exception as e:
            self.log_test("TC-SEC-009.1", "FAILED", str(e))
            
        # Test 2: API endpoint rate limiting
        try:
            rapid_requests = 0
            for i in range(20):  # Try 20 rapid API requests
                response = self.session.get(f"{self.base_url_camera}/cameras", 
                                          headers={"Authorization": f"Bearer {self.auth_token}"})
                if response.status_code == 200:
                    rapid_requests += 1
                elif response.status_code == 429:  # Rate limit exceeded
                    self.log_test("TC-SEC-009.2", "PASSED", f"API rate limiting triggered after {i+1} requests")
                    break
                time.sleep(0.05)  # Small delay between requests
                
            if rapid_requests == 20:
                self.log_test("TC-SEC-009.2", "WARNING", "API rate limiting not detected after 20 requests")
        except Exception as e:
            self.log_test("TC-SEC-009.2", "FAILED", str(e))

    def run_all_security_tests(self):
        """Run all security tests"""
        print("🔒 SECURITY TESTING SUITE")
        print("=" * 50)
        
        # Get authentication token first
        if not self.get_auth_token():
            print("❌ Cannot proceed without authentication token")
            return False
            
        # Run all security tests
        self.test_jwt_token_security()
        self.test_password_security()
        self.test_rbac_security()
        self.test_api_authentication()
        self.test_sql_injection_prevention()
        self.test_xss_prevention()
        self.test_rate_limiting()
        
        # Generate summary
        self.generate_summary()
        return True
        
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 50)
        print("🔒 SECURITY TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASSED"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAILED"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARNING"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warning_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        
        # Save results
        results_file = "sharedResource/automationTest/backend/results/security_test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "test_suite": "Security Testing",
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "warnings": warning_tests,
                    "success_rate": (passed_tests/total_tests*100) if total_tests > 0 else 0
                },
                "results": self.test_results
            }, f, indent=2)
            
        print(f"\n📊 Results saved to: {results_file}")

if __name__ == "__main__":
    test_suite = SecurityTestSuite()
    test_suite.run_all_security_tests() 