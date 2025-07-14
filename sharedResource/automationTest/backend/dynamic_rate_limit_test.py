#!/usr/bin/env python3
"""
Dynamic Rate Limiting Test Suite
Tests the dynamic rate limiting functionality in beCamera service
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# Configuration
AUTH_URL = "http://localhost:3001/api/v1/auth"
CAMERA_URL = "http://localhost:3002/api/v1"
ADMIN_URL = "http://localhost:3002/admin"

class DynamicRateLimitTester:
    def __init__(self):
        self.access_token = None
        self.test_results = []
        
    def log_test(self, test_name, passed, details=""):
        """Log test result"""
        status = "PASSED" if passed else "FAILED"
        print(f"[{status}] {test_name}: {details}")
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
    def setup_auth(self):
        """Setup authentication"""
        try:
            # Register a test user
            register_data = {
                "username": "ratelimituser",
                "password": "RateLimit123!",
                "confirmPassword": "RateLimit123!",
                "email": "ratelimit@test.com",
                "registrationCode": "REG001"
            }
            
            response = requests.post(f"{AUTH_URL}/register", json=register_data)
            if response.status_code == 201:
                self.access_token = response.json()["data"]["accessToken"]
                self.log_test("AUTH-SETUP", True, "User registered and token obtained")
                return True
            elif response.status_code == 400 and "already exists" in response.text:
                # User exists, try to login
                login_data = {
                    "username": "ratelimituser",
                    "password": "RateLimit123!"
                }
                response = requests.post(f"{AUTH_URL}/login", json=login_data)
                if response.status_code == 200:
                    self.access_token = response.json()["data"]["accessToken"]
                    self.log_test("AUTH-SETUP", True, "User logged in and token obtained")
                    return True
                    
            self.log_test("AUTH-SETUP", False, f"Failed to setup auth: {response.status_code}")
            return False
            
        except Exception as e:
            self.log_test("AUTH-SETUP", False, f"Exception: {str(e)}")
            return False
    
    def test_get_current_rate_limit(self):
        """Test getting current rate limit"""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{ADMIN_URL}/rate-limit", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "rate_limit" in data:
                    self.log_test("RATE-GET-001", True, f"Current rate limit: {data['rate_limit']}")
                    return data["rate_limit"]
                else:
                    self.log_test("RATE-GET-001", False, "Rate limit not found in response")
                    return None
            else:
                self.log_test("RATE-GET-001", False, f"Status: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("RATE-GET-001", False, f"Exception: {str(e)}")
            return None
    
    def test_set_rate_limit(self, new_limit):
        """Test setting new rate limit"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            data = {
                "rate_limit": new_limit,
                "description": "Test rate limit change"
            }
            
            response = requests.put(f"{ADMIN_URL}/rate-limit", headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("rate_limit") == new_limit:
                    self.log_test("RATE-SET-001", True, f"Rate limit set to: {new_limit}")
                    return True
                else:
                    self.log_test("RATE-SET-001", False, f"Rate limit not updated correctly")
                    return False
            else:
                self.log_test("RATE-SET-001", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("RATE-SET-001", False, f"Exception: {str(e)}")
            return False
    
    def test_rate_limit_enforcement(self, expected_limit):
        """Test that rate limiting is enforced with current limit"""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Make requests until we hit rate limit
            success_count = 0
            rate_limited = False
            
            for i in range(20):  # Try more than the limit
                response = requests.get(f"{CAMERA_URL}/cameras", headers=headers)
                
                if response.status_code == 200:
                    success_count += 1
                elif response.status_code == 429:
                    rate_limited = True
                    break
                else:
                    self.log_test("RATE-ENFORCE-001", False, f"Unexpected status: {response.status_code}")
                    return False
                
                time.sleep(0.1)  # Small delay between requests
            
            # Parse expected limit (e.g., "10/minute" -> 10)
            expected_count = int(expected_limit.split('/')[0])
            
            if rate_limited and success_count <= expected_count:
                self.log_test("RATE-ENFORCE-001", True, f"Rate limited after {success_count} requests (limit: {expected_count})")
                return True
            else:
                self.log_test("RATE-ENFORCE-001", False, f"Rate limiting not working: {success_count} requests, expected max {expected_count}")
                return False
                
        except Exception as e:
            self.log_test("RATE-ENFORCE-001", False, f"Exception: {str(e)}")
            return False
    
    def test_rate_limit_recovery(self):
        """Test that rate limiting resets after window"""
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # First, hit the rate limit
            for i in range(15):
                response = requests.get(f"{CAMERA_URL}/cameras", headers=headers)
                if response.status_code == 429:
                    break
                time.sleep(0.1)
            
            # Wait for rate limit window to reset (1 minute)
            print("Waiting 65 seconds for rate limit window to reset...")
            time.sleep(65)
            
            # Try again
            response = requests.get(f"{CAMERA_URL}/cameras", headers=headers)
            
            if response.status_code == 200:
                self.log_test("RATE-RECOVERY-001", True, "Rate limit recovered after window")
                return True
            else:
                self.log_test("RATE-RECOVERY-001", False, f"Rate limit not recovered: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("RATE-RECOVERY-001", False, f"Exception: {str(e)}")
            return False
    
    def test_invalid_rate_limit_format(self):
        """Test setting invalid rate limit format"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            data = {
                "rate_limit": "invalid_format",
                "description": "Invalid format test"
            }
            
            response = requests.put(f"{ADMIN_URL}/rate-limit", headers=headers, json=data)
            
            if response.status_code == 422:  # Validation error
                self.log_test("RATE-VALIDATE-001", True, "Invalid rate limit format rejected")
                return True
            else:
                self.log_test("RATE-VALIDATE-001", False, f"Invalid format accepted: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("RATE-VALIDATE-001", False, f"Exception: {str(e)}")
            return False
    
    def test_unauthorized_access(self):
        """Test unauthorized access to rate limit admin endpoints"""
        try:
            # Test without token
            response = requests.get(f"{ADMIN_URL}/rate-limit")
            if response.status_code == 401:
                self.log_test("RATE-AUTH-001", True, "Unauthorized access blocked")
                return True
            else:
                self.log_test("RATE-AUTH-001", False, f"Unauthorized access allowed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("RATE-AUTH-001", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all dynamic rate limiting tests"""
        print("Starting Dynamic Rate Limiting Test Suite")
        print("=" * 50)
        
        # Setup authentication
        if not self.setup_auth():
            print("Failed to setup authentication. Exiting.")
            return False
        
        # Test 1: Get current rate limit
        current_limit = self.test_get_current_rate_limit()
        if not current_limit:
            return False
        
        # Test 2: Set new rate limit
        new_limit = "15/minute"
        if not self.test_set_rate_limit(new_limit):
            return False
        
        # Test 3: Verify rate limit was set
        updated_limit = self.test_get_current_rate_limit()
        if updated_limit != new_limit:
            self.log_test("RATE-VERIFY-001", False, f"Rate limit not updated: {updated_limit}")
            return False
        else:
            self.log_test("RATE-VERIFY-001", True, f"Rate limit verified: {updated_limit}")
        
        # Test 4: Test rate limit enforcement
        if not self.test_rate_limit_enforcement(new_limit):
            return False
        
        # Test 5: Test invalid format
        if not self.test_invalid_rate_limit_format():
            return False
        
        # Test 6: Test unauthorized access
        if not self.test_unauthorized_access():
            return False
        
        # Test 7: Test rate limit recovery (optional - takes time)
        print("\nTesting rate limit recovery (this will take 65 seconds)...")
        if not self.test_rate_limit_recovery():
            return False
        
        # Reset rate limit to original
        self.test_set_rate_limit(current_limit)
        
        return True
    
    def save_results(self):
        """Save test results to file"""
        results = {
            "test_suite": "Dynamic Rate Limiting",
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.test_results),
            "passed": sum(1 for r in self.test_results if r["passed"]),
            "failed": sum(1 for r in self.test_results if not r["passed"]),
            "results": self.test_results
        }
        
        os.makedirs("results", exist_ok=True)
        with open("results/dynamic_rate_limit_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: results/dynamic_rate_limit_results.json")

def main():
    tester = DynamicRateLimitTester()
    
    try:
        success = tester.run_all_tests()
        
        # Print summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        total = len(tester.test_results)
        passed = sum(1 for r in tester.test_results if r["passed"])
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        tester.save_results()
        
        return 0 if failed == 0 else 1
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        return 1
    except Exception as e:
        print(f"\nTest failed with exception: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 