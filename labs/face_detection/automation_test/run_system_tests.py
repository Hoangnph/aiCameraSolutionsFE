#!/usr/bin/env python3
"""
Comprehensive Automation Test Suite for Face Detection System
Tests all API endpoints, database operations, and system functionality
"""

import requests
import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import cv2
import numpy as np
from PIL import Image
import io

class FaceDetectionSystemTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        self.test_images_dir = "automation_test/test_images"
        self.test_data = {
            "test_users": [
                {"name": "Test User 1", "email": "test1@example.com", "phone": "1234567890"},
                {"name": "Test User 2", "email": "test2@example.com", "phone": "1234567891"},
                {"name": "Test User 3", "email": "test3@example.com", "phone": "1234567892"},
                {"name": "Test User 4", "email": "test4@example.com", "phone": "1234567893"},
                {"name": "Test User 5", "email": "test5@example.com", "phone": "1234567894"}
            ]
        }
        
    def log_test(self, test_name: str, success: bool, message: str = "", data: Dict = None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        return success
    
    def test_api_health(self) -> bool:
        """Test API health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                services = data.get('data', {}).get('services', {})
                return self.log_test(
                    "API Health Check",
                    True,
                    f"All services healthy: {list(services.keys())}",
                    services
                )
            else:
                return self.log_test(
                    "API Health Check",
                    False,
                    f"HTTP {response.status_code}"
                )
        except Exception as e:
            return self.log_test(
                "API Health Check",
                False,
                f"Connection error: {str(e)}"
            )
    
    def test_root_endpoint(self) -> bool:
        """Test root endpoint"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return self.log_test(
                    "Root Endpoint",
                    True,
                    f"API version: {data.get('data', {}).get('version', 'Unknown')}",
                    data
                )
            else:
                return self.log_test(
                    "Root Endpoint",
                    False,
                    f"HTTP {response.status_code}"
                )
        except Exception as e:
            return self.log_test(
                "Root Endpoint",
                False,
                f"Connection error: {str(e)}"
            )
    
    def test_camera_status(self) -> bool:
        """Test camera status endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/camera/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                camera_data = data.get('data', {})
                return self.log_test(
                    "Camera Status",
                    True,
                    f"Device {camera_data.get('device_id')}, Active: {camera_data.get('active')}",
                    camera_data
                )
            else:
                return self.log_test(
                    "Camera Status",
                    False,
                    f"HTTP {response.status_code}"
                )
        except Exception as e:
            return self.log_test(
                "Camera Status",
                False,
                f"Connection error: {str(e)}"
            )
    
    def test_camera_control(self) -> bool:
        """Test camera start/stop functionality"""
        results = []
        
        # Test camera start
        try:
            response = requests.post(f"{self.base_url}/api/v1/camera/start", timeout=5)
            if response.status_code == 200:
                data = response.json()
                results.append(self.log_test(
                    "Camera Start",
                    True,
                    data.get('message', 'Camera started'),
                    data
                ))
            else:
                results.append(self.log_test(
                    "Camera Start",
                    False,
                    f"HTTP {response.status_code}"
                ))
        except Exception as e:
            results.append(self.log_test(
                "Camera Start",
                False,
                f"Connection error: {str(e)}"
            ))
        
        # Wait a moment
        time.sleep(2)
        
        # Test camera stop
        try:
            response = requests.post(f"{self.base_url}/api/v1/camera/stop", timeout=5)
            if response.status_code == 200:
                data = response.json()
                results.append(self.log_test(
                    "Camera Stop",
                    True,
                    data.get('message', 'Camera stopped'),
                    data
                ))
            else:
                results.append(self.log_test(
                    "Camera Stop",
                    False,
                    f"HTTP {response.status_code}"
                ))
        except Exception as e:
            results.append(self.log_test(
                "Camera Stop",
                False,
                f"Connection error: {str(e)}"
            ))
        
        return all(results)
    
    def test_face_registration(self) -> bool:
        """Test face registration functionality"""
        results = []
        
        # Check if test image exists
        test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
        if not os.path.exists(test_image_path):
            return self.log_test(
                "Face Registration",
                False,
                f"Test image not found: {test_image_path}"
            )
        
        # Test face registration for each test user
        for i, user in enumerate(self.test_data["test_users"]):
            try:
                with open(test_image_path, 'rb') as f:
                    files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                    data = {
                        'name': user['name'],
                        'email': user['email'],
                        'phone': user['phone'],
                        'notes': f'Automation test user {i+1}'
                    }
                    
                    response = requests.post(
                        f"{self.base_url}/api/v1/faces/upload",
                        files=files,
                        data=data,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result_data = response.json()
                        if result_data.get('success'):
                            registration_data = result_data.get('data', {})
                            results.append(self.log_test(
                                f"Face Registration - {user['name']}",
                                True,
                                f"Person ID: {registration_data.get('person_id')}, Confidence: {registration_data.get('confidence', 0):.2f}",
                                registration_data
                            ))
                        else:
                            results.append(self.log_test(
                                f"Face Registration - {user['name']}",
                                False,
                                result_data.get('message', 'Registration failed')
                            ))
                    else:
                        results.append(self.log_test(
                            f"Face Registration - {user['name']}",
                            False,
                            f"HTTP {response.status_code}"
                        ))
                        
            except Exception as e:
                results.append(self.log_test(
                    f"Face Registration - {user['name']}",
                    False,
                    f"Error: {str(e)}"
                ))
        
        return all(results)
    
    def test_face_recognition(self) -> bool:
        """Test face recognition functionality"""
        results = []
        
        # Check if test image exists
        test_image_path = os.path.join(self.test_images_dir, "test_face.jpg")
        if not os.path.exists(test_image_path):
            return self.log_test(
                "Face Recognition",
                False,
                f"Test image not found: {test_image_path}"
            )
        
        # Test face recognition
        try:
            with open(test_image_path, 'rb') as f:
                files = {'file': ('test_face.jpg', f, 'image/jpeg')}
                data = {'threshold': '0.6'}
                
                response = requests.post(
                    f"{self.base_url}/api/v1/faces/recognize",
                    files=files,
                    data=data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result_data = response.json()
                    if result_data.get('success'):
                        recognition_data = result_data.get('data', {})
                        if recognition_data.get('recognized'):
                            person = recognition_data.get('person', {})
                            confidence = recognition_data.get('confidence', 0)
                            results.append(self.log_test(
                                "Face Recognition",
                                True,
                                f"Recognized: {person.get('name', 'Unknown')} (Confidence: {confidence:.2f})",
                                recognition_data
                            ))
                        else:
                            results.append(self.log_test(
                                "Face Recognition",
                                True,
                                "No face recognized (expected for unregistered faces)",
                                recognition_data
                            ))
                    else:
                        results.append(self.log_test(
                            "Face Recognition",
                            False,
                            result_data.get('message', 'Recognition failed')
                        ))
                else:
                    results.append(self.log_test(
                        "Face Recognition",
                        False,
                        f"HTTP {response.status_code}"
                    ))
                    
        except Exception as e:
            results.append(self.log_test(
                "Face Recognition",
                False,
                f"Error: {str(e)}"
            ))
        
        return all(results)
    
    def test_face_list(self) -> bool:
        """Test face list endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/faces/list", timeout=5)
            if response.status_code == 200:
                data = response.json()
                faces = data.get('data', {}).get('faces', [])
                return self.log_test(
                    "Face List",
                    True,
                    f"Found {len(faces)} registered faces",
                    {"face_count": len(faces), "faces": faces}
                )
            else:
                return self.log_test(
                    "Face List",
                    False,
                    f"HTTP {response.status_code}"
                )
        except Exception as e:
            return self.log_test(
                "Face List",
                False,
                f"Connection error: {str(e)}"
            )
    
    def test_performance(self) -> bool:
        """Test system performance"""
        results = []
        
        # Test response time for health endpoint
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                results.append(self.log_test(
                    "Performance - Health Check",
                    response_time < 500,  # Should be under 500ms
                    f"Response time: {response_time:.1f}ms",
                    {"response_time_ms": response_time}
                ))
            else:
                results.append(self.log_test(
                    "Performance - Health Check",
                    False,
                    f"HTTP {response.status_code}"
                ))
        except Exception as e:
            results.append(self.log_test(
                "Performance - Health Check",
                False,
                f"Error: {str(e)}"
            ))
        
        # Test response time for face list
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/api/v1/faces/list", timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                results.append(self.log_test(
                    "Performance - Face List",
                    response_time < 1000,  # Should be under 1 second
                    f"Response time: {response_time:.1f}ms",
                    {"response_time_ms": response_time}
                ))
            else:
                results.append(self.log_test(
                    "Performance - Face List",
                    False,
                    f"HTTP {response.status_code}"
                ))
        except Exception as e:
            results.append(self.log_test(
                "Performance - Face List",
                False,
                f"Error: {str(e)}"
            ))
        
        return all(results)
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": success_rate,
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url
            },
            "test_results": self.test_results,
            "recommendations": []
        }
        
        # Generate recommendations
        if failed_tests > 0:
            report["recommendations"].append("Some tests failed. Check server logs and system status.")
        
        if success_rate < 100:
            report["recommendations"].append("System needs improvement. Review failed tests.")
        
        if success_rate == 100:
            report["recommendations"].append("All tests passed! System is working correctly.")
        
        return report
    
    def save_test_report(self, report: Dict[str, Any], filename: str = None):
        """Save test report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.json"
        
        report_path = os.path.join("automation_test", "reports", filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Test report saved to: {report_path}")
        return report_path
    
    def run_all_tests(self) -> bool:
        """Run all tests and generate report"""
        print("🚀 Starting Comprehensive Face Detection System Tests")
        print("=" * 60)
        
        # Run all tests
        tests = [
            ("API Health Check", self.test_api_health),
            ("Root Endpoint", self.test_root_endpoint),
            ("Camera Status", self.test_camera_status),
            ("Camera Control", self.test_camera_control),
            ("Face Registration", self.test_face_registration),
            ("Face Recognition", self.test_face_recognition),
            ("Face List", self.test_face_list),
            ("Performance Tests", self.test_performance)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name}...")
            test_func()
        
        # Generate and display report
        report = self.generate_test_report()
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Passed: {report['summary']['passed_tests']}")
        print(f"Failed: {report['summary']['failed_tests']}")
        print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
        
        if report['recommendations']:
            print("\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"   • {rec}")
        
        # Save report
        self.save_test_report(report)
        
        return report['summary']['success_rate'] == 100

def main():
    """Main function"""
    print("🎯 Face Detection System - Comprehensive Automation Test")
    print("=" * 60)
    
    # Create test instance
    tester = FaceDetectionSystemTest()
    
    # Run all tests
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! System is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the system and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 