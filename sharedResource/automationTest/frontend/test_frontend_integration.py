#!/usr/bin/env python3
"""
Frontend Integration Test Suite
Tests the integration between frontend and backend services
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class FrontendIntegrationTest:
    def __init__(self):
        self.base_urls = {
            'frontend': 'http://localhost:3000',
            'beauth': 'http://localhost:3001',
            'becamera': 'http://localhost:3002',
            'websocket': 'ws://localhost:3004'
        }
        self.test_results = []
        self.start_time = datetime.now()

    def log_test(self, test_name: str, success: bool, message: str = "", data: Any = None):
        """Log test result"""
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if data and not success:
            print(f"   Data: {json.dumps(data, indent=2)}")

    def test_frontend_accessibility(self) -> bool:
        """Test if frontend is accessible"""
        try:
            response = requests.get(f"{self.base_urls['frontend']}", timeout=10)
            success = response.status_code == 200
            self.log_test(
                "Frontend Accessibility",
                success,
                f"Status: {response.status_code}"
            )
            return success
        except Exception as e:
            self.log_test(
                "Frontend Accessibility",
                False,
                f"Error: {str(e)}"
            )
            return False

    def test_backend_apis_accessible(self) -> bool:
        """Test if backend APIs are accessible"""
        apis_to_test = [
            ('beAuth Health', f"{self.base_urls['beauth']}/health"),
            ('beCamera Health', f"{self.base_urls['becamera']}/health"),
            ('beCamera Test Cameras', f"{self.base_urls['becamera']}/api/v1/test/cameras"),
            ('beCamera Test Workers', f"{self.base_urls['becamera']}/api/v1/test/workers/status"),
        ]
        
        all_success = True
        for name, url in apis_to_test:
            try:
                response = requests.get(url, timeout=10)
                success = response.status_code == 200
                self.log_test(
                    f"Backend API - {name}",
                    success,
                    f"Status: {response.status_code}"
                )
                if not success:
                    all_success = False
            except Exception as e:
                self.log_test(
                    f"Backend API - {name}",
                    False,
                    f"Error: {str(e)}"
                )
                all_success = False
        
        return all_success

    def test_camera_api_integration(self) -> bool:
        """Test camera API integration"""
        try:
            # Test getting cameras
            response = requests.get(f"{self.base_urls['becamera']}/api/v1/test/cameras", timeout=10)
            if response.status_code != 200:
                self.log_test("Camera API Integration", False, f"Failed to get cameras: {response.status_code}")
                return False
            
            cameras_data = response.json()
            if not cameras_data.get('success'):
                self.log_test("Camera API Integration", False, "API response indicates failure")
                return False
            
            cameras = cameras_data.get('data', [])
            self.log_test(
                "Camera API Integration",
                True,
                f"Successfully retrieved {len(cameras)} cameras"
            )
            
            # Test worker pool status
            response = requests.get(f"{self.base_urls['becamera']}/api/v1/test/workers/status", timeout=10)
            if response.status_code != 200:
                self.log_test("Worker Pool API Integration", False, f"Failed to get worker status: {response.status_code}")
                return False
            
            workers_data = response.json()
            if not workers_data.get('success'):
                self.log_test("Worker Pool API Integration", False, "API response indicates failure")
                return False
            
            workers = workers_data.get('data', {})
            total_workers = workers.get('total_workers', 0)
            self.log_test(
                "Worker Pool API Integration",
                True,
                f"Successfully retrieved worker pool status with {total_workers} workers"
            )
            
            return True
            
        except Exception as e:
            self.log_test("API Integration", False, f"Error: {str(e)}")
            return False

    def test_api_response_format(self) -> bool:
        """Test API response format consistency"""
        try:
            # Test camera API format
            response = requests.get(f"{self.base_urls['becamera']}/api/v1/test/cameras", timeout=10)
            cameras_data = response.json()
            
            # Check required fields
            required_fields = ['success', 'data', 'count']
            missing_fields = [field for field in required_fields if field not in cameras_data]
            
            if missing_fields:
                self.log_test("API Response Format", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check camera object structure
            if cameras_data['data']:
                camera = cameras_data['data'][0]
                camera_fields = ['id', 'name', 'ip_address', 'rtsp_url', 'status', 'created_at']
                missing_camera_fields = [field for field in camera_fields if field not in camera]
                
                if missing_camera_fields:
                    self.log_test("Camera Object Format", False, f"Missing camera fields: {missing_camera_fields}")
                    return False
            
            # Test worker API format
            response = requests.get(f"{self.base_urls['becamera']}/api/v1/test/workers/status", timeout=10)
            workers_data = response.json()
            
            if not workers_data.get('success'):
                self.log_test("Worker API Response Format", False, "Worker API response indicates failure")
                return False
            
            workers = workers_data.get('data', {})
            worker_fields = ['workers', 'total_workers', 'idle_workers', 'busy_workers']
            missing_worker_fields = [field for field in worker_fields if field not in workers]
            
            if missing_worker_fields:
                self.log_test("Worker Object Format", False, f"Missing worker fields: {missing_worker_fields}")
                return False
            
            self.log_test("API Response Format", True, "All APIs return consistent format")
            return True
            
        except Exception as e:
            self.log_test("API Response Format", False, f"Error: {str(e)}")
            return False

    def test_cors_headers(self) -> bool:
        """Test CORS headers for frontend-backend communication"""
        try:
            # Test CORS headers on camera API with GET request
            response = requests.get(
                f"{self.base_urls['becamera']}/api/v1/test/cameras", 
                headers={"Origin": "http://localhost:3000"},
                timeout=10
            )
            
            # Check for CORS headers
            cors_headers = [
                'access-control-allow-origin',
                'access-control-allow-credentials'
            ]
            
            missing_headers = [header for header in cors_headers if header not in response.headers]
            
            if missing_headers:
                self.log_test("CORS Headers", False, f"Missing CORS headers: {missing_headers}")
                return False
            
            # Check if origin is allowed
            allow_origin = response.headers.get('access-control-allow-origin', '')
            if allow_origin not in ['*', 'http://localhost:3000']:
                self.log_test("CORS Headers", False, f"Origin not allowed: {allow_origin}")
                return False
            
            self.log_test("CORS Headers", True, f"CORS headers present: {allow_origin}")
            return True
            
        except Exception as e:
            self.log_test("CORS Headers", False, f"Error: {str(e)}")
            return False

    def test_error_handling(self) -> bool:
        """Test error handling in APIs"""
        try:
            # Test invalid endpoint
            response = requests.get(f"{self.base_urls['becamera']}/api/v1/test/nonexistent", timeout=10)
            
            if response.status_code == 404:
                self.log_test("Error Handling - 404", True, "Properly handles non-existent endpoints")
            else:
                self.log_test("Error Handling - 404", False, f"Unexpected status code: {response.status_code}")
                return False
            
            # Test invalid camera ID
            response = requests.get(f"{self.base_urls['becamera']}/api/v1/test/cameras/999999", timeout=10)
            
            if response.status_code in [404, 400]:
                self.log_test("Error Handling - Invalid ID", True, "Properly handles invalid camera ID")
            else:
                self.log_test("Error Handling - Invalid ID", False, f"Unexpected status code: {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Error Handling", False, f"Error: {str(e)}")
            return False

    def test_performance(self) -> bool:
        """Test API response times"""
        try:
            # Test camera API response time
            start_time = time.time()
            response = requests.get(f"{self.base_urls['becamera']}/api/v1/test/cameras", timeout=10)
            response_time = time.time() - start_time
            
            if response_time < 2.0:  # Should respond within 2 seconds
                self.log_test("Performance - Camera API", True, f"Response time: {response_time:.2f}s")
            else:
                self.log_test("Performance - Camera API", False, f"Slow response time: {response_time:.2f}s")
                return False
            
            # Test worker API response time
            start_time = time.time()
            response = requests.get(f"{self.base_urls['becamera']}/api/v1/test/workers/status", timeout=10)
            response_time = time.time() - start_time
            
            if response_time < 2.0:
                self.log_test("Performance - Worker API", True, f"Response time: {response_time:.2f}s")
            else:
                self.log_test("Performance - Worker API", False, f"Slow response time: {response_time:.2f}s")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Performance", False, f"Error: {str(e)}")
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        print("🚀 Starting Frontend Integration Tests")
        print("=" * 50)
        
        tests = [
            ("Frontend Accessibility", self.test_frontend_accessibility),
            ("Backend APIs Accessible", self.test_backend_apis_accessible),
            ("Camera API Integration", self.test_camera_api_integration),
            ("API Response Format", self.test_api_response_format),
            ("CORS Headers", self.test_cors_headers),
            ("Error Handling", self.test_error_handling),
            ("Performance", self.test_performance),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test exception: {str(e)}")
        
        # Generate summary
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        summary = {
            'total_tests': total,
            'passed': passed,
            'failed': total - passed,
            'success_rate': (passed / total) * 100 if total > 0 else 0,
            'duration': duration,
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'results': self.test_results
        }
        
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Duration: {duration:.2f}s")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the results above.")
        
        return summary

def main():
    """Main function to run the test suite"""
    test_suite = FrontendIntegrationTest()
    results = test_suite.run_all_tests()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"frontend_integration_test_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to: {results_file}")
    
    # Exit with appropriate code
    if results['passed'] == results['total_tests']:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 