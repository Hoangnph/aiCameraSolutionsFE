#!/usr/bin/env python3
"""
🧪 System Integration Tests - AI Camera Counting System
📅 Updated: 2025-07-16
👥 Maintainer: QA Team

Test Cases: INTEGRATION-001 to INTEGRATION-020
Priority: Critical
Type: System Integration
Standardized Response Format: v2.0
"""

import requests
import json
import sys
import time
from datetime import datetime
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class SystemIntegrationTest:
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        self.config = self.load_config()
        self.auth_url = self.config['test_environment']['base_urls']['auth_api']
        self.camera_url = self.config['test_environment']['base_urls']['camera_api']
        self.session = requests.Session()
        self.access_token = None
        self.test_user = None
        self.test_cameras = []

    def load_config(self):
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
        result = {
            'test_name': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {message}")
        if details:
            print(f"   Details: {details}")

    def validate_standard_response(self, response_data, expected_success=True):
        """Validate standardized response format"""
        required_fields = ['success', 'timestamp', 'request_id']
        
        if expected_success:
            required_fields.extend(['data', 'message'])
        else:
            required_fields.extend(['error'])
        
        for field in required_fields:
            if field not in response_data:
                return False, f"Missing required field: {field}"
        
        if expected_success and not response_data['success']:
            return False, "Expected success response but got error"
        
        if not expected_success and response_data['success']:
            return False, "Expected error response but got success"
        
        return True, "Response format valid"

    def test_environment_health(self):
        """Test all service health endpoints"""
        test_name = "INTEGRATION-001"
        try:
            # Test auth service health
            auth_health_url = self.auth_url.replace('/api/v1', '') + '/health'
            auth_resp = self.session.get(auth_health_url, timeout=10)
            
            if auth_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Auth service health check failed: {auth_resp.status_code}")
                return False
            
            # Test camera service health
            camera_health_url = self.camera_url.replace('/api/v1', '') + '/health'
            camera_resp = self.session.get(camera_health_url, timeout=10)
            
            if camera_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Camera service health check failed: {camera_resp.status_code}")
                return False
            
            camera_data = camera_resp.json()
            required_fields = ['status', 'database', 'redis']
            for field in required_fields:
                if field not in camera_data:
                    self.log_test(test_name, "FAIL", f"Camera health missing field: {field}")
                    return False
            
            self.log_test(test_name, "PASS", "All services healthy", 
                         f"Auth: {auth_resp.status_code}, Camera: {camera_resp.status_code}")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_user_registration_flow(self):
        """Test complete user registration flow"""
        test_name = "INTEGRATION-002"
        try:
            timestamp = int(time.time())
            self.test_user = {
                "username": f"integrationtest{timestamp}",
                "email": f"integrationtest{timestamp}@example.com",
                "password": "Integration123!",
                "confirmPassword": "Integration123!",
                "firstName": "Integration",
                "lastName": "Test",
                "registrationCode": "REG001"
            }
            
            # Register user
            reg_resp = self.session.post(
                f"{self.auth_url}/auth/register",
                json=self.test_user,
                timeout=10
            )
            
            if reg_resp.status_code not in [200, 201]:
                self.log_test(test_name, "FAIL", f"Registration failed: {reg_resp.status_code} - {reg_resp.text}")
                return False
            
            data = reg_resp.json()
            is_valid, error_msg = self.validate_standard_response(data, True)
            if not is_valid:
                self.log_test(test_name, "FAIL", f"Invalid registration response: {error_msg}")
                return False
            
            if 'data' in data and 'accessToken' in data['data']:
                self.access_token = data['data']['accessToken']
            
            self.log_test(test_name, "PASS", "User registration flow successful")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_user_login_flow(self):
        """Test user login flow"""
        test_name = "INTEGRATION-003"
        try:
            if not self.test_user:
                self.log_test(test_name, "FAIL", "No test user available")
                return False
            
            # Login user
            login_resp = self.session.post(
                f"{self.auth_url}/auth/login",
                json={"email": self.test_user["email"], "password": self.test_user["password"]},
                timeout=10
            )
            
            if login_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Login failed: {login_resp.status_code} - {login_resp.text}")
                return False
            
            data = login_resp.json()
            is_valid, error_msg = self.validate_standard_response(data, True)
            if not is_valid:
                self.log_test(test_name, "FAIL", f"Invalid login response: {error_msg}")
                return False
            
            if 'data' in data and 'accessToken' in data['data']:
                self.access_token = data['data']['accessToken']
            
            self.log_test(test_name, "PASS", "User login flow successful")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_token_validation(self):
        """Test JWT token validation across services"""
        test_name = "INTEGRATION-004"
        try:
            if not self.access_token:
                self.log_test(test_name, "FAIL", "No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Test token validation with auth service
            verify_resp = self.session.post(
                f"{self.auth_url}/auth/verify",
                headers=headers,
                timeout=10
            )
            
            if verify_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Token verification failed: {verify_resp.status_code}")
                return False
            
            # Test token usage with camera service
            camera_resp = self.session.get(
                f"{self.camera_url}/cameras",
                headers=headers,
                timeout=10
            )
            
            if camera_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Camera service token validation failed: {camera_resp.status_code}")
                return False
            
            self.log_test(test_name, "PASS", "Token validation successful across services")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_camera_crud_flow(self):
        """Test complete camera CRUD flow"""
        test_name = "INTEGRATION-005"
        try:
            if not self.access_token:
                self.log_test(test_name, "FAIL", "No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Create camera
            camera_data = {
                "name": "Integration Test Camera",
                "ip_address": "192.168.1.200",
                "rtsp_url": "rtsp://192.168.1.200:554/stream",
                "status": "offline"
            }
            
            create_resp = self.session.post(
                f"{self.camera_url}/cameras",
                json=camera_data,
                headers=headers,
                timeout=10
            )
            
            if create_resp.status_code not in [200, 201]:
                self.log_test(test_name, "FAIL", f"Camera creation failed: {create_resp.status_code}")
                return False
            
            create_data = create_resp.json()
            is_valid, error_msg = self.validate_standard_response(create_data, True)
            if not is_valid:
                self.log_test(test_name, "FAIL", f"Invalid create response: {error_msg}")
                return False
            
            camera_id = create_data['data']['id']
            self.test_cameras.append(camera_id)
            
            # Read camera
            read_resp = self.session.get(
                f"{self.camera_url}/cameras/{camera_id}",
                headers=headers,
                timeout=10
            )
            
            if read_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Camera read failed: {read_resp.status_code}")
                return False
            
            # Update camera
            update_data = {"name": "Updated Integration Camera", "status": "active"}
            update_resp = self.session.put(
                f"{self.camera_url}/cameras/{camera_id}",
                json=update_data,
                headers=headers,
                timeout=10
            )
            
            if update_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Camera update failed: {update_resp.status_code}")
                return False
            
            # Delete camera
            delete_resp = self.session.delete(
                f"{self.camera_url}/cameras/{camera_id}",
                headers=headers,
                timeout=10
            )
            
            if delete_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Camera delete failed: {delete_resp.status_code}")
                return False
            
            self.test_cameras.remove(camera_id)
            
            self.log_test(test_name, "PASS", "Complete camera CRUD flow successful")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_camera_processing_flow(self):
        """Test camera processing start/stop flow"""
        test_name = "INTEGRATION-006"
        try:
            if not self.access_token:
                self.log_test(test_name, "FAIL", "No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Create a camera for processing test
            camera_data = {
                "name": "Processing Test Camera",
                "ip_address": "192.168.1.201",
                "rtsp_url": "rtsp://192.168.1.201:554/stream",
                "status": "active"
            }
            
            create_resp = self.session.post(
                f"{self.camera_url}/cameras",
                json=camera_data,
                headers=headers,
                timeout=10
            )
            
            if create_resp.status_code not in [200, 201]:
                self.log_test(test_name, "FAIL", f"Camera creation for processing failed: {create_resp.status_code}")
                return False
            
            camera_id = create_resp.json()['data']['id']
            self.test_cameras.append(camera_id)
            
            # Start processing
            start_resp = self.session.post(
                f"{self.camera_url}/cameras/{camera_id}/start",
                headers=headers,
                timeout=10
            )
            
            if start_resp.status_code not in [200, 201]:
                self.log_test(test_name, "FAIL", f"Start processing failed: {start_resp.status_code}")
                return False
            
            # Check processing status
            status_resp = self.session.get(
                f"{self.camera_url}/cameras/{camera_id}/status",
                headers=headers,
                timeout=10
            )
            
            if status_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Status check failed: {status_resp.status_code}")
                return False
            
            # Stop processing
            stop_resp = self.session.post(
                f"{self.camera_url}/cameras/{camera_id}/stop",
                headers=headers,
                timeout=10
            )
            
            if stop_resp.status_code not in [200, 201]:
                self.log_test(test_name, "FAIL", f"Stop processing failed: {stop_resp.status_code}")
                return False
            
            self.log_test(test_name, "PASS", "Camera processing flow successful")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_analytics_flow(self):
        """Test analytics data flow"""
        test_name = "INTEGRATION-007"
        try:
            if not self.access_token:
                self.log_test(test_name, "FAIL", "No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Test count data retrieval
            counts_resp = self.session.get(
                f"{self.camera_url}/counts",
                headers=headers,
                timeout=10
            )
            
            if counts_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Count data retrieval failed: {counts_resp.status_code}")
                return False
            
            counts_data = counts_resp.json()
            is_valid, error_msg = self.validate_standard_response(counts_data, True)
            if not is_valid:
                self.log_test(test_name, "FAIL", f"Invalid counts response: {error_msg}")
                return False
            
            # Test analytics summary
            analytics_resp = self.session.get(
                f"{self.camera_url}/analytics/summary",
                headers=headers,
                timeout=10
            )
            
            if analytics_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Analytics summary failed: {analytics_resp.status_code}")
                return False
            
            analytics_data = analytics_resp.json()
            is_valid, error_msg = self.validate_standard_response(analytics_data, True)
            if not is_valid:
                self.log_test(test_name, "FAIL", f"Invalid analytics response: {error_msg}")
                return False
            
            self.log_test(test_name, "PASS", "Analytics flow successful")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_worker_pool_integration(self):
        """Test worker pool integration"""
        test_name = "INTEGRATION-008"
        try:
            if not self.access_token:
                self.log_test(test_name, "FAIL", "No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Test worker pool status
            worker_resp = self.session.get(
                f"{self.camera_url}/workers/status",
                headers=headers,
                timeout=10
            )
            
            if worker_resp.status_code != 200:
                self.log_test(test_name, "FAIL", f"Worker pool status failed: {worker_resp.status_code}")
                return False
            
            worker_data = worker_resp.json()
            is_valid, error_msg = self.validate_standard_response(worker_data, True)
            if not is_valid:
                self.log_test(test_name, "FAIL", f"Invalid worker response: {error_msg}")
                return False
            
            self.log_test(test_name, "PASS", "Worker pool integration successful")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_error_handling_integration(self):
        """Test error handling across services"""
        test_name = "INTEGRATION-009"
        try:
            if not self.access_token:
                self.log_test(test_name, "FAIL", "No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Test invalid camera ID
            invalid_resp = self.session.get(
                f"{self.camera_url}/cameras/99999",
                headers=headers,
                timeout=10
            )
            
            if invalid_resp.status_code == 404:
                data = invalid_resp.json()
                is_valid, error_msg = self.validate_standard_response(data, False)
                if is_valid:
                    self.log_test(test_name, "PASS", "Error handling integration successful")
                    return True
                else:
                    self.log_test(test_name, "FAIL", f"Invalid error response format: {error_msg}")
                    return False
            else:
                self.log_test(test_name, "FAIL", f"Expected 404 error, got {invalid_resp.status_code}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_rate_limiting_integration(self):
        """Test rate limiting across services"""
        test_name = "INTEGRATION-010"
        try:
            if not self.access_token:
                self.log_test(test_name, "FAIL", "No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Make multiple requests to test rate limiting
            rate_limit_headers_found = True
            
            for i in range(3):
                resp = self.session.get(
                    f"{self.camera_url}/cameras",
                    headers=headers,
                    timeout=10
                )
                
                if resp.status_code == 200:
                    # Check for rate limiting headers
                    required_headers = ['X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset']
                    for header in required_headers:
                        if header not in resp.headers:
                            rate_limit_headers_found = False
                            break
                else:
                    self.log_test(test_name, "FAIL", f"Request {i+1} failed: {resp.status_code}")
                    return False
                
                time.sleep(0.5)  # Small delay between requests
            
            if rate_limit_headers_found:
                self.log_test(test_name, "PASS", "Rate limiting integration successful")
                return True
            else:
                self.log_test(test_name, "FAIL", "Rate limiting headers missing")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def cleanup_test_data(self):
        """Clean up test data"""
        test_name = "INTEGRATION-CLEANUP"
        if not self.access_token or not self.test_cameras:
            return True
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            for camera_id in self.test_cameras:
                try:
                    resp = self.session.delete(
                        f"{self.camera_url}/cameras/{camera_id}",
                        headers=headers,
                        timeout=10
                    )
                    if resp.status_code == 200:
                        print(f"   Cleaned up camera ID: {camera_id}")
                except Exception as e:
                    print(f"   Warning: Could not clean up camera {camera_id}: {e}")
            
            self.log_test(test_name, "PASS", "Test cleanup completed")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Cleanup failed: {str(e)}")
            return False

    def save_results(self):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        results = {
            'test_suite': 'System Integration Tests (v2.0)',
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': duration,
            'total_tests': len(self.test_results),
            'passed_tests': len([r for r in self.test_results if r['status'] == 'PASS']),
            'failed_tests': len([r for r in self.test_results if r['status'] == 'FAIL']),
            'success_rate': f"{len([r for r in self.test_results if r['status'] == 'PASS']) / len(self.test_results) * 100:.1f}%" if self.test_results else "0%",
            'results': self.test_results
        }
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
        os.makedirs(results_dir, exist_ok=True)
        results_file = os.path.join(results_dir, 'system_integration_test_results_v2.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📊 Results saved to: {results_file}")
        return results

    def run_all_tests(self):
        print("==========================================")
        print("🧪 SYSTEM INTEGRATION TESTS (v2.0)")
        print("AI Camera Counting System")
        print("Standardized Response Format")
        print("==========================================")
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Run all integration tests
        tests = [
            self.test_environment_health,
            self.test_user_registration_flow,
            self.test_user_login_flow,
            self.test_token_validation,
            self.test_camera_crud_flow,
            self.test_camera_processing_flow,
            self.test_analytics_flow,
            self.test_worker_pool_integration,
            self.test_error_handling_integration,
            self.test_rate_limiting_integration
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        # Cleanup test data
        self.cleanup_test_data()
        
        print("")
        print("==========================================")
        print("📊 INTEGRATION TEST SUMMARY")
        print("==========================================")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All integration tests passed! System is fully integrated.")
        else:
            print("⚠️  Some integration tests failed. Please review the results.")
        
        print("==========================================")
        
        # Save results
        self.save_results()

def main():
    test_suite = SystemIntegrationTest()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main() 