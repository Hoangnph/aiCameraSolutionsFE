#!/usr/bin/env python3
"""
🧪 Camera Management API Tests - AI Camera Counting System
📅 Updated: 2025-07-16
👥 Maintainer: QA Team

Test Cases: CAMERA-001 to CAMERA-015
Priority: High
Type: API Integration
Standardized Response Format: v2.0
"""

import requests
import json
import sys
import time
from datetime import datetime
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class CameraAPITest:
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        self.config = self.load_config()
        self.base_url = self.config['test_environment']['base_urls']['camera_api']
        self.auth_url = self.config['test_environment']['base_urls']['auth_api']
        self.session = requests.Session()
        self.access_token = None
        self.camera_id = None
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

    def register_and_login_user(self):
        """Đăng ký và đăng nhập user để lấy access token"""
        test_name = "CAMERA-000"
        try:
            timestamp = int(time.time())
            test_user = {
                "username": f"cameratest{timestamp}",
                "email": f"cameratest{timestamp}@example.com",
                "password": "Test123!",
                "confirmPassword": "Test123!",
                "firstName": "Camera",
                "lastName": "Test",
                "registrationCode": "REG001"
            }
            
            # Đăng ký
            reg_resp = self.session.post(
                f"{self.auth_url}/auth/register",
                json=test_user,
                timeout=10
            )
            
            if reg_resp.status_code in [200, 201]:
                data = reg_resp.json()
                # Validate response format
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid registration response format: {error_msg}")
                    return False
                
                if 'data' in data and 'accessToken' in data['data']:
                    self.access_token = data['data']['accessToken']
                self.log_test(test_name, "PASS", "User registration for camera test successful")
            else:
                self.log_test(test_name, "FAIL", f"User registration failed: {reg_resp.status_code} - {reg_resp.text}")
                return False
            
            # Đăng nhập (dự phòng)
            if not self.access_token:
                login_resp = self.session.post(
                    f"{self.auth_url}/auth/login",
                    json={"email": test_user["email"], "password": test_user["password"]},
                    timeout=10
                )
                if login_resp.status_code == 200:
                    data = login_resp.json()
                    if 'data' in data and 'accessToken' in data['data']:
                        self.access_token = data['data']['accessToken']
            
            if not self.access_token:
                self.log_test(test_name, "FAIL", "Could not obtain access token for camera test")
                return False
            
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_health_check(self):
        """Test health check endpoint"""
        test_name = "CAMERA-001"
        try:
            resp = self.session.get(f"{self.base_url.replace('/api/v1', '')}/health", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                required_fields = ['status', 'timestamp', 'service', 'database', 'redis']
                for field in required_fields:
                    if field not in data:
                        self.log_test(test_name, "FAIL", f"Health check missing field: {field}")
                        return False
                self.log_test(test_name, "PASS", "Health check successful", f"Status: {data['status']}")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Health check failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_create_camera(self):
        """Test camera creation with standardized response format"""
        test_name = "CAMERA-002"
        if not self.access_token:
            self.log_test(test_name, "FAIL", "No access token available for create camera test")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            camera_data = {
                "name": "Test Camera API",
                "ip_address": "192.168.1.100",
                "rtsp_url": "rtsp://192.168.1.100:554/stream",
                "status": "offline"
            }
            resp = self.session.post(
                f"{self.base_url}/cameras",
                json=camera_data,
                headers=headers,
                timeout=10
            )
            
            if resp.status_code in [200, 201]:
                data = resp.json()
                # Validate standardized response format
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid response format: {error_msg}")
                    return False
                
                # Extract camera ID from response
                if 'data' in data and 'id' in data['data']:
                    self.camera_id = data['data']['id']
                    self.test_cameras.append(self.camera_id)
                else:
                    self.log_test(test_name, "FAIL", "Camera ID not found in response")
                    return False
                
                self.log_test(test_name, "PASS", "Camera created successfully", f"ID: {self.camera_id}")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Camera creation failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_list_cameras(self):
        """Test camera listing with standardized response format"""
        test_name = "CAMERA-003"
        if not self.access_token:
            self.log_test(test_name, "FAIL", "No access token available for list cameras test")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            resp = self.session.get(f"{self.base_url}/cameras", headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                # Validate standardized response format
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid response format: {error_msg}")
                    return False
                
                cameras = data.get('data', [])
                self.log_test(test_name, "PASS", "Camera list fetched successfully", f"Count: {len(cameras)}")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Camera list fetch failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_get_camera_by_id(self):
        """Test getting camera by ID"""
        test_name = "CAMERA-004"
        if not self.access_token or not self.camera_id:
            self.log_test(test_name, "FAIL", "No access token or camera_id available")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            resp = self.session.get(f"{self.base_url}/cameras/{self.camera_id}", headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                # Validate response format
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid response format: {error_msg}")
                    return False
                
                self.log_test(test_name, "PASS", "Camera retrieved successfully")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Camera retrieval failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_update_camera(self):
        """Test camera update with standardized response format"""
        test_name = "CAMERA-005"
        if not self.access_token or not self.camera_id:
            self.log_test(test_name, "FAIL", "No access token or camera_id available for update camera test")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            update_data = {
                "name": "Updated Camera Name",
                "status": "maintenance"
            }
            resp = self.session.put(
                f"{self.base_url}/cameras/{self.camera_id}",
                json=update_data,
                headers=headers,
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                # Validate standardized response format
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid response format: {error_msg}")
                    return False
                
                self.log_test(test_name, "PASS", "Camera updated successfully")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Camera update failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_update_camera_status(self):
        """Test camera status update"""
        test_name = "CAMERA-006"
        if not self.access_token or not self.camera_id:
            self.log_test(test_name, "FAIL", "No access token or camera_id available")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            status_data = {"status": "active"}
            resp = self.session.patch(
                f"{self.base_url}/cameras/{self.camera_id}/status",
                json=status_data,
                headers=headers,
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid response format: {error_msg}")
                    return False
                
                self.log_test(test_name, "PASS", "Camera status updated successfully")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Camera status update failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_get_count_data(self):
        """Test count data retrieval"""
        test_name = "CAMERA-007"
        if not self.access_token:
            self.log_test(test_name, "FAIL", "No access token available")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            resp = self.session.get(f"{self.base_url}/counts", headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid response format: {error_msg}")
                    return False
                
                self.log_test(test_name, "PASS", "Count data retrieved successfully")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Count data retrieval failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_get_analytics_summary(self):
        """Test analytics summary retrieval"""
        test_name = "CAMERA-008"
        if not self.access_token:
            self.log_test(test_name, "FAIL", "No access token available")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            resp = self.session.get(f"{self.base_url}/analytics/summary", headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid response format: {error_msg}")
                    return False
                
                self.log_test(test_name, "PASS", "Analytics summary retrieved successfully")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Analytics summary retrieval failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_worker_pool_status(self):
        """Test worker pool status endpoint"""
        test_name = "CAMERA-009"
        if not self.access_token:
            self.log_test(test_name, "FAIL", "No access token available")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            resp = self.session.get(f"{self.base_url}/workers/status", headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid response format: {error_msg}")
                    return False
                
                self.log_test(test_name, "PASS", "Worker pool status retrieved successfully")
                return True
            else:
                self.log_test(test_name, "FAIL", f"Worker pool status retrieval failed: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_camera_processing_control(self):
        """Test camera processing start/stop"""
        test_name = "CAMERA-010"
        if not self.access_token or not self.camera_id:
            self.log_test(test_name, "FAIL", "No access token or camera_id available")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Test start processing
            start_resp = self.session.post(
                f"{self.base_url}/cameras/{self.camera_id}/start",
                headers=headers,
                timeout=10
            )
            
            if start_resp.status_code in [200, 201]:
                data = start_resp.json()
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid start response format: {error_msg}")
                    return False
            
            # Test stop processing
            stop_resp = self.session.post(
                f"{self.base_url}/cameras/{self.camera_id}/stop",
                headers=headers,
                timeout=10
            )
            
            if stop_resp.status_code in [200, 201]:
                data = stop_resp.json()
                is_valid, error_msg = self.validate_standard_response(data, True)
                if not is_valid:
                    self.log_test(test_name, "FAIL", f"Invalid stop response format: {error_msg}")
                    return False
            
            self.log_test(test_name, "PASS", "Camera processing control successful")
            return True
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_error_handling(self):
        """Test error handling with standardized error format"""
        test_name = "CAMERA-011"
        if not self.access_token:
            self.log_test(test_name, "FAIL", "No access token available")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Test invalid camera ID
            resp = self.session.get(f"{self.base_url}/cameras/99999", headers=headers, timeout=10)
            
            if resp.status_code == 404:
                data = resp.json()
                is_valid, error_msg = self.validate_standard_response(data, False)
                if is_valid:
                    self.log_test(test_name, "PASS", "Error handling with standardized format successful")
                    return True
                else:
                    self.log_test(test_name, "FAIL", f"Invalid error response format: {error_msg}")
                    return False
            else:
                self.log_test(test_name, "FAIL", f"Expected 404 error, got {resp.status_code}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def test_rate_limiting_headers(self):
        """Test rate limiting headers"""
        test_name = "CAMERA-012"
        if not self.access_token:
            self.log_test(test_name, "FAIL", "No access token available")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            resp = self.session.get(f"{self.base_url}/cameras", headers=headers, timeout=10)
            
            if resp.status_code == 200:
                # Check for rate limiting headers
                rate_limit_headers = ['X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset']
                missing_headers = []
                
                for header in rate_limit_headers:
                    if header not in resp.headers:
                        missing_headers.append(header)
                
                if not missing_headers:
                    self.log_test(test_name, "PASS", "Rate limiting headers present")
                    return True
                else:
                    self.log_test(test_name, "FAIL", f"Missing rate limiting headers: {missing_headers}")
                    return False
            else:
                self.log_test(test_name, "FAIL", f"Request failed: {resp.status_code}")
                return False
        except Exception as e:
            self.log_test(test_name, "FAIL", f"Exception: {str(e)}")
            return False

    def cleanup_test_cameras(self):
        """Clean up test cameras"""
        test_name = "CAMERA-CLEANUP"
        if not self.access_token or not self.test_cameras:
            return True
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            for camera_id in self.test_cameras:
                try:
                    resp = self.session.delete(
                        f"{self.base_url}/cameras/{camera_id}",
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
            'test_suite': 'Camera Management API Tests (v2.0)',
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
        results_file = os.path.join(results_dir, 'camera_api_test_results_v2.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📊 Results saved to: {results_file}")
        return results

    def run_all_tests(self):
        print("==========================================")
        print("🧪 CAMERA MANAGEMENT API TESTS (v2.0)")
        print("AI Camera Counting System")
        print("Standardized Response Format")
        print("==========================================")
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Đăng ký và đăng nhập user test
        if not self.register_and_login_user():
            print("❌ Cannot run camera tests without access token!")
            return
        
        # Run all tests
        tests = [
            self.test_health_check,
            self.test_create_camera,
            self.test_list_cameras,
            self.test_get_camera_by_id,
            self.test_update_camera,
            self.test_update_camera_status,
            self.test_get_count_data,
            self.test_get_analytics_summary,
            self.test_worker_pool_status,
            self.test_camera_processing_control,
            self.test_error_handling,
            self.test_rate_limiting_headers
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        # Cleanup test data
        self.cleanup_test_cameras()
        
        print("")
        print("==========================================")
        print("📊 TEST SUMMARY")
        print("==========================================")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All camera API tests passed!")
        else:
            print("⚠️  Some tests failed. Please review the results.")
        
        print("==========================================")
        
        # Save results
        self.save_results()

def main():
    test_suite = CameraAPITest()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main() 